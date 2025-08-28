#!/usr/bin/env python3
"""
Repository Analyzer for Mendicant AI.
Performs comprehensive health checks on repositories.
"""

import asyncio
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.config import HEALTH_CHECK_CATEGORIES
from src.utils import setup_logging, safe_run, parse_flake8_output

logger = setup_logging(__name__, level="INFO")

class RepositoryAnalyzer:
    """Comprehensive repository health analyzer."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        self.results = {
            "repository": str(repo_path),
            "health_score": 0,
            "checks": {},
            "summary": {},
            "recommendations": []
        }
    
    async def analyze(self) -> Dict[str, Any]:
        """Run all health checks on the repository."""
        logger.info(f"Starting analysis of repository: {self.repo_path}")
        
        # Run all check categories
        for category in HEALTH_CHECK_CATEGORIES:
            logger.info(f"Running {category} checks...")
            
            if category == "code_quality":
                await self._check_code_quality()
            elif category == "security":
                await self._check_security()
            elif category == "testing":
                await self._check_testing()
            elif category == "documentation":
                await self._check_documentation()
            elif category == "dependencies":
                await self._check_dependencies()
            elif category == "performance":
                await self._check_performance()
        
        # Calculate overall health score
        self._calculate_health_score()
        
        # Generate recommendations
        self._generate_recommendations()
        
        logger.info(f"Analysis complete. Health score: {self.results['health_score']}/100")
        return self.results
    
    async def _check_code_quality(self):
        """Check code quality using various linters."""
        checks = []
        
        # Python files - Flake8
        python_files = list(self.repo_path.rglob("*.py"))
        if python_files:
            for py_file in python_files[:10]:  # Limit for demo
                try:
                    returncode, stdout, stderr = safe_run(
                        ["flake8", str(py_file)],
                        cwd=self.repo_path
                    )
                    
                    if returncode == 0:
                        checks.append({
                            "check_name": f"flake8_{py_file.name}",
                            "status": "passed",
                            "severity": "info",
                            "message": "No linting issues found",
                            "file_path": str(py_file.relative_to(self.repo_path))
                        })
                    else:
                        issues = parse_flake8_output(stdout)
                        for issue in issues:
                            checks.append({
                                "check_name": f"flake8_{issue['code']}",
                                "status": "failed",
                                "severity": "medium",
                                "message": issue['message'],
                                "file_path": str(py_file.relative_to(self.repo_path)),
                                "line_number": issue['line']
                            })
                            
                except Exception as e:
                    logger.warning(f"Failed to check {py_file}: {e}")
        
        # JavaScript/TypeScript files - ESLint (if available)
        js_files = list(self.repo_path.rglob("*.js")) + list(self.repo_path.rglob("*.ts"))
        if js_files:
            try:
                returncode, stdout, stderr = safe_run(
                    ["npx", "eslint", "--format", "json"] + [str(f) for f in js_files[:5]],
                    cwd=self.repo_path
                )
                
                if returncode == 0:
                    checks.append({
                        "check_name": "eslint_check",
                        "status": "passed",
                        "severity": "info",
                        "message": "No ESLint issues found"
                    })
                else:
                    checks.append({
                        "check_name": "eslint_check",
                        "status": "failed",
                        "severity": "medium",
                        "message": "ESLint issues detected",
                        "details": {"stderr": stderr}
                    })
                    
            except Exception as e:
                logger.debug(f"ESLint not available: {e}")
        
        # Check for long/complex functions
        for py_file in python_files[:5]:
            complexity_issues = await self._check_complexity(py_file)
            checks.extend(complexity_issues)
        
        self.results["checks"]["code_quality"] = checks
    
    async def _check_security(self):
        """Check for security vulnerabilities."""
        checks = []
        
        # Check for secrets in code
        secret_patterns = [
            (r'api[_-]?key\s*[:=]\s*["\'][^"\']+["\']', "API key detected"),
            (r'password\s*[:=]\s*["\'][^"\']+["\']', "Hardcoded password detected"),
            (r'secret\s*[:=]\s*["\'][^"\']+["\']', "Secret detected"),
            (r'token\s*[:=]\s*["\'][^"\']+["\']', "Token detected"),
        ]
        
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".py", ".js", ".ts", ".yml", ".yaml", ".json"]:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    import re
                    for pattern, message in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            checks.append({
                                "check_name": "secret_detection",
                                "status": "failed",
                                "severity": "high",
                                "message": message,
                                "file_path": str(file_path.relative_to(self.repo_path))
                            })
                            
                except Exception as e:
                    logger.debug(f"Could not read {file_path}: {e}")
        
        # Check for vulnerable dependencies (Python)
        requirements_files = list(self.repo_path.rglob("requirements*.txt"))
        for req_file in requirements_files:
            try:
                returncode, stdout, stderr = safe_run(
                    ["safety", "check", "-r", str(req_file)],
                    cwd=self.repo_path
                )
                
                if returncode == 0:
                    checks.append({
                        "check_name": f"safety_check_{req_file.name}",
                        "status": "passed",
                        "severity": "info",
                        "message": "No known vulnerabilities in dependencies"
                    })
                else:
                    checks.append({
                        "check_name": f"safety_check_{req_file.name}",
                        "status": "failed",
                        "severity": "high",
                        "message": "Vulnerable dependencies detected",
                        "details": {"output": stdout}
                    })
                    
            except Exception as e:
                logger.debug(f"Safety check failed for {req_file}: {e}")
        
        self.results["checks"]["security"] = checks
    
    async def _check_testing(self):
        """Check testing setup and quality."""
        checks = []
        
        # Look for test files
        test_files = []
        for pattern in ["test_*.py", "*_test.py", "tests/**/*.py"]:
            test_files.extend(self.repo_path.rglob(pattern))
        
        if not test_files:
            checks.append({
                "check_name": "test_files_exist",
                "status": "failed",
                "severity": "high",
                "message": "No test files found in repository"
            })
        else:
            checks.append({
                "check_name": "test_files_exist",
                "status": "passed",
                "severity": "info",
                "message": f"Found {len(test_files)} test files"
            })
        
        # Check for pytest configuration
        pytest_configs = list(self.repo_path.rglob("pytest.ini")) + \
                        list(self.repo_path.rglob("pyproject.toml")) + \
                        list(self.repo_path.rglob("setup.cfg"))
        
        if pytest_configs:
            checks.append({
                "check_name": "pytest_config",
                "status": "passed",
                "severity": "info",
                "message": "Pytest configuration found"
            })
        else:
            checks.append({
                "check_name": "pytest_config",
                "status": "warning",
                "severity": "low",
                "message": "No pytest configuration found"
            })
        
        # Try to run tests if they exist
        if test_files:
            try:
                returncode, stdout, stderr = safe_run(
                    ["python", "-m", "pytest", "--collect-only", "-q"],
                    cwd=self.repo_path,
                    timeout=30
                )
                
                if returncode == 0:
                    # Count collected tests
                    lines = stdout.split('\n')
                    test_count = sum(1 for line in lines if '<Function' in line or '<Method' in line)
                    
                    checks.append({
                        "check_name": "test_collection",
                        "status": "passed",
                        "severity": "info", 
                        "message": f"Successfully collected {test_count} tests"
                    })
                else:
                    checks.append({
                        "check_name": "test_collection",
                        "status": "failed",
                        "severity": "medium",
                        "message": "Failed to collect tests",
                        "details": {"stderr": stderr}
                    })
                    
            except Exception as e:
                logger.debug(f"Test collection failed: {e}")
        
        self.results["checks"]["testing"] = checks
    
    async def _check_documentation(self):
        """Check documentation quality."""
        checks = []
        
        # Check for README
        readme_files = list(self.repo_path.glob("README*"))
        if readme_files:
            readme_file = readme_files[0]
            content = readme_file.read_text(encoding='utf-8', errors='ignore')
            
            # Check README sections
            required_sections = ["installation", "usage", "contributing"]
            missing_sections = []
            
            for section in required_sections:
                if section.lower() not in content.lower():
                    missing_sections.append(section)
            
            if missing_sections:
                checks.append({
                    "check_name": "readme_completeness",
                    "status": "warning",
                    "severity": "low",
                    "message": f"README missing sections: {', '.join(missing_sections)}"
                })
            else:
                checks.append({
                    "check_name": "readme_completeness",
                    "status": "passed",
                    "severity": "info",
                    "message": "README contains all recommended sections"
                })
        else:
            checks.append({
                "check_name": "readme_exists",
                "status": "failed",
                "severity": "medium",
                "message": "No README file found"
            })
        
        # Check for LICENSE
        license_files = list(self.repo_path.glob("LICENSE*"))
        if license_files:
            checks.append({
                "check_name": "license_exists",
                "status": "passed",
                "severity": "info",
                "message": "License file found"
            })
        else:
            checks.append({
                "check_name": "license_exists",
                "status": "warning",
                "severity": "low",
                "message": "No license file found"
            })
        
        self.results["checks"]["documentation"] = checks
    
    async def _check_dependencies(self):
        """Check dependency management."""
        checks = []
        
        # Python dependencies
        requirements_files = list(self.repo_path.rglob("requirements*.txt"))
        pyproject_files = list(self.repo_path.rglob("pyproject.toml"))
        
        if requirements_files or pyproject_files:
            checks.append({
                "check_name": "dependency_files",
                "status": "passed",
                "severity": "info",
                "message": "Dependency files found"
            })
        else:
            checks.append({
                "check_name": "dependency_files",
                "status": "warning",
                "severity": "medium",
                "message": "No dependency management files found"
            })
        
        # JavaScript dependencies
        package_json = self.repo_path / "package.json"
        if package_json.exists():
            checks.append({
                "check_name": "npm_dependencies",
                "status": "passed",
                "severity": "info",
                "message": "package.json found"
            })
            
            # Check for lock file
            if (self.repo_path / "package-lock.json").exists() or \
               (self.repo_path / "yarn.lock").exists():
                checks.append({
                    "check_name": "dependency_lock",
                    "status": "passed",
                    "severity": "info",
                    "message": "Dependency lock file found"
                })
            else:
                checks.append({
                    "check_name": "dependency_lock",
                    "status": "warning",
                    "severity": "low",
                    "message": "No dependency lock file found"
                })
        
        self.results["checks"]["dependencies"] = checks
    
    async def _check_performance(self):
        """Check for performance issues."""
        checks = []
        
        # Check for large files
        large_files = []
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size > 10 * 1024 * 1024:  # 10MB
                        large_files.append((str(file_path.relative_to(self.repo_path)), size))
                except:
                    pass
        
        if large_files:
            checks.append({
                "check_name": "large_files",
                "status": "warning",
                "severity": "low",
                "message": f"Found {len(large_files)} large files (>10MB)",
                "details": {"files": large_files}
            })
        else:
            checks.append({
                "check_name": "large_files",
                "status": "passed",
                "severity": "info",
                "message": "No unusually large files found"
            })
        
        # Check .gitignore
        gitignore = self.repo_path / ".gitignore"
        if gitignore.exists():
            checks.append({
                "check_name": "gitignore_exists",
                "status": "passed",
                "severity": "info",
                "message": ".gitignore file found"
            })
        else:
            checks.append({
                "check_name": "gitignore_exists",
                "status": "warning",
                "severity": "low",
                "message": "No .gitignore file found"
            })
        
        self.results["checks"]["performance"] = checks
    
    async def _check_complexity(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check code complexity for a Python file."""
        checks = []
        
        try:
            # Simple complexity check - count lines in functions
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            in_function = False
            function_start = 0
            function_name = ""
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                if stripped.startswith('def '):
                    if in_function and i - function_start > 50:  # Function longer than 50 lines
                        checks.append({
                            "check_name": "function_complexity",
                            "status": "warning",
                            "severity": "low",
                            "message": f"Function '{function_name}' is long ({i - function_start} lines)",
                            "file_path": str(file_path.relative_to(self.repo_path)),
                            "line_number": function_start + 1
                        })
                    
                    in_function = True
                    function_start = i
                    function_name = stripped.split('(')[0].replace('def ', '')
                
                elif stripped and not stripped.startswith('#') and not line.startswith(' ') and not line.startswith('\t'):
                    if in_function and i - function_start > 50:
                        checks.append({
                            "check_name": "function_complexity",
                            "status": "warning",
                            "severity": "low",
                            "message": f"Function '{function_name}' is long ({i - function_start} lines)",
                            "file_path": str(file_path.relative_to(self.repo_path)),
                            "line_number": function_start + 1
                        })
                    in_function = False
            
        except Exception as e:
            logger.debug(f"Complexity check failed for {file_path}: {e}")
        
        return checks
    
    def _calculate_health_score(self):
        """Calculate overall repository health score (0-100)."""
        total_checks = 0
        passed_checks = 0
        
        for category, checks in self.results["checks"].items():
            for check in checks:
                total_checks += 1
                if check["status"] == "passed":
                    passed_checks += 1
                elif check["status"] == "warning":
                    passed_checks += 0.5  # Partial credit for warnings
        
        if total_checks > 0:
            self.results["health_score"] = int((passed_checks / total_checks) * 100)
        else:
            self.results["health_score"] = 0
        
        # Generate summary
        summary = {}
        for category, checks in self.results["checks"].items():
            category_stats = {
                "total": len(checks),
                "passed": len([c for c in checks if c["status"] == "passed"]),
                "failed": len([c for c in checks if c["status"] == "failed"]),
                "warnings": len([c for c in checks if c["status"] == "warning"])
            }
            summary[category] = category_stats
        
        self.results["summary"] = summary
    
    def _generate_recommendations(self):
        """Generate actionable recommendations based on failed checks."""
        recommendations = []
        
        for category, checks in self.results["checks"].items():
            failed_checks = [c for c in checks if c["status"] == "failed"]
            warning_checks = [c for c in checks if c["status"] == "warning"]
            
            if category == "code_quality" and failed_checks:
                recommendations.append({
                    "category": "code_quality",
                    "priority": "high",
                    "title": "Fix code quality issues",
                    "description": f"Found {len(failed_checks)} linting issues that should be addressed",
                    "action": "Run autopep8 and fix remaining manual issues"
                })
            
            if category == "security" and failed_checks:
                recommendations.append({
                    "category": "security", 
                    "priority": "critical",
                    "title": "Address security vulnerabilities",
                    "description": "Security issues detected that need immediate attention",
                    "action": "Review and fix all security issues before deploying"
                })
            
            if category == "testing" and failed_checks:
                recommendations.append({
                    "category": "testing",
                    "priority": "high", 
                    "title": "Improve test coverage",
                    "description": "Testing setup needs improvement",
                    "action": "Add tests and ensure they run properly"
                })
            
            if category == "documentation" and (failed_checks or warning_checks):
                recommendations.append({
                    "category": "documentation",
                    "priority": "medium",
                    "title": "Improve documentation",
                    "description": "Documentation is incomplete or missing",
                    "action": "Add missing README sections and documentation"
                })
        
        self.results["recommendations"] = recommendations

async def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Analyze repository health")
    parser.add_argument("repository", help="Path to repository to analyze")
    parser.add_argument("--output", "-o", help="Output file for results (JSON)")
    parser.add_argument("--format", choices=["json", "summary"], default="summary",
                       help="Output format")
    
    args = parser.parse_args()
    
    repo_path = Path(args.repository)
    if not repo_path.exists():
        print(f"Error: Repository path {repo_path} does not exist")
        return 1
    
    analyzer = RepositoryAnalyzer(repo_path)
    results = await analyzer.analyze()
    
    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:
        # Summary format
        output = f"""
Repository Health Report: {results['repository']}
Health Score: {results['health_score']}/100

Summary by Category:
"""
        for category, stats in results['summary'].items():
            output += f"  {category.title()}: {stats['passed']}/{stats['total']} passed"
            if stats['warnings'] > 0:
                output += f" ({stats['warnings']} warnings)"
            if stats['failed'] > 0:
                output += f" ({stats['failed']} failed)"
            output += "\n"
        
        if results['recommendations']:
            output += "\nRecommendations:\n"
            for rec in results['recommendations']:
                output += f"  [{rec['priority'].upper()}] {rec['title']}: {rec['description']}\n"
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"Results written to {args.output}")
    else:
        print(output)
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
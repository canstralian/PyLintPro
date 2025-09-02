# src/agents/advanced.py

"""
Advanced and specialized agents with complex capabilities.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union
from .core import BaseAgent, AgentContext, claude_api_call


class SystemDesignAgent(BaseAgent):
    """
    Agent for system design with interactive clarification and Mermaid.js diagrams.
    
    Maintains conversation history and produces architectural diagrams.
    """
    
    def __init__(self):
        super().__init__(name="SystemDesign", max_steps=5)
        self.conversation_history = []
        self.requirements = {}
        self.clarifications_needed = []
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Analyze system design requirements."""
        if isinstance(input_data, dict):
            requirement = input_data.get("requirement", "")
            clarification = input_data.get("clarification", "")
        else:
            requirement = str(input_data)
            clarification = ""
        
        # Add to conversation history
        if requirement:
            self.conversation_history.append({"role": "user", "content": requirement})
        if clarification:
            self.conversation_history.append({"role": "user", "content": f"Clarification: {clarification}"})
        
        return f"System design requirement: {requirement or clarification}"
    
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """Plan system design approach."""
        step = len(context)
        
        if step == 0:
            return "Analyze requirements and identify clarifications needed:\n" \
                   "1. Functional requirements\n" \
                   "2. Non-functional requirements (scale, performance)\n" \
                   "3. Technical constraints\n" \
                   "4. Integration points"
        elif step == 1:
            return "Generate system architecture:\n" \
                   "1. High-level components\n" \
                   "2. Component interactions\n" \
                   "3. Data flow\n" \
                   "4. Technology stack recommendations"
        elif step == 2:
            return "Create Mermaid.js diagram representing the system architecture"
        else:
            return "Finalize design document with diagrams and explanations"
    
    def act(self, action_plan: str) -> str:
        """Execute system design step."""
        step = len(getattr(self, '_context_history', []))
        
        if step == 0:
            # Analyze requirements
            conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
            prompt = f"""
            Analyze these system design requirements:
            
            {conversation}
            
            Identify:
            1. Core functional requirements
            2. Non-functional requirements (performance, scalability, etc.)
            3. Technical constraints
            4. Missing information that needs clarification
            5. Assumptions that should be validated
            
            If critical information is missing, list specific questions to ask.
            """
            return claude_api_call(prompt)
            
        elif step == 1:
            # Generate architecture
            analysis = context[0].result if context else ""
            prompt = f"""
            Based on this requirements analysis:
            {analysis}
            
            Design a system architecture including:
            1. High-level system components
            2. Component responsibilities
            3. Inter-component communication
            4. Data storage strategy
            5. Technology stack recommendations
            6. Scalability considerations
            
            Provide a detailed architectural design.
            """
            return claude_api_call(prompt)
            
        elif step == 2:
            # Create Mermaid diagram
            architecture = context[1].result if len(context) > 1 else ""
            prompt = f"""
            Create a Mermaid.js component diagram for this system architecture:
            
            {architecture}
            
            Generate a Mermaid.js diagram showing:
            - System components
            - Data flow between components
            - External integrations
            - User interactions
            
            Provide only the Mermaid.js code in a code block.
            """
            return claude_api_call(prompt)
        
        else:
            # Finalize design document
            architecture = context[1].result if len(context) > 1 else ""
            diagram = context[2].result if len(context) > 2 else ""
            
            prompt = f"""
            Create a comprehensive system design document including:
            
            Architecture:
            {architecture}
            
            Diagram:
            {diagram}
            
            Format as a complete design document with:
            1. Executive Summary
            2. System Overview
            3. Architecture Details
            4. Component Specifications
            5. Technology Stack
            6. Deployment Strategy
            7. Scalability Plan
            8. Security Considerations
            """
            return claude_api_call(prompt)
    
    def is_task_complete(self, result: Any, context: List[AgentContext]) -> bool:
        """Check if design is complete or needs clarification."""
        # Could implement logic to detect if clarifications are needed
        return len(context) >= 3  # Complete after architecture, diagram, and documentation


class TestSuiteWriterAgent(BaseAgent):
    """
    Agent that analyzes project structure and generates comprehensive test suites.
    
    Reads project files and generates organized unit and integration tests.
    """
    
    def __init__(self, project_path: str = "."):
        super().__init__(name="TestSuiteWriter", max_steps=4)
        self.project_path = Path(project_path)
        self.project_structure = {}
        self.test_plan = {}
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Analyze project structure and identify files to test."""
        if isinstance(input_data, dict):
            path = input_data.get("project_path", self.project_path)
            focus_files = input_data.get("focus_files", [])
        else:
            path = self.project_path
            focus_files = []
        
        self.project_structure = self._analyze_project_structure(Path(path))
        
        structure_summary = self._summarize_structure()
        return f"Project structure analysis:\n{structure_summary}"
    
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """Plan test suite generation approach."""
        step = len(context)
        
        if step == 0:
            return "Analyze project files and plan test coverage:\n" \
                   "1. Identify testable functions and classes\n" \
                   "2. Determine test types needed (unit, integration)\n" \
                   "3. Plan test file organization\n" \
                   "4. Identify dependencies and mocking needs"
        elif step == 1:
            return "Generate unit tests for core functionality"
        elif step == 2:
            return "Generate integration tests for component interactions"
        else:
            return "Organize tests and create test runner configuration"
    
    def act(self, action_plan: str) -> str:
        """Execute test generation step."""
        step = len(getattr(self, '_context_history', []))
        
        if step == 0:
            # Analyze for test planning
            structure = self._format_structure_for_analysis()
            prompt = f"""
            Analyze this Python project structure and plan comprehensive test coverage:
            
            {structure}
            
            For each module, identify:
            1. Functions/classes that need unit tests
            2. Integration points that need testing
            3. Edge cases and error conditions
            4. Mock requirements for external dependencies
            5. Test file organization strategy
            
            Provide a detailed test plan.
            """
            return claude_api_call(prompt)
            
        elif step == 1:
            # Generate unit tests
            test_plan = context[0].result if context else ""
            structure = self._format_structure_for_analysis()
            
            prompt = f"""
            Generate comprehensive unit tests based on this test plan:
            {test_plan}
            
            For this project structure:
            {structure}
            
            Create pytest unit tests including:
            1. Test classes for each module
            2. Test methods for each function/method
            3. Edge cases and error handling
            4. Fixtures and mocks where needed
            5. Proper assertions and test data
            
            Organize tests logically and include docstrings.
            """
            return claude_api_call(prompt)
            
        elif step == 2:
            # Generate integration tests
            unit_tests = context[1].result if len(context) > 1 else ""
            
            prompt = f"""
            Generate integration tests that complement these unit tests:
            {unit_tests[:1000]}...
            
            Create integration tests for:
            1. Component interactions
            2. API endpoints (if applicable)
            3. Database operations (if applicable)
            4. File I/O operations
            5. External service integrations
            
            Focus on testing how components work together.
            """
            return claude_api_call(prompt)
        
        else:
            # Create test organization and configuration
            unit_tests = context[1].result if len(context) > 1 else ""
            integration_tests = context[2].result if len(context) > 2 else ""
            
            prompt = f"""
            Create a complete test suite organization including:
            
            Unit Tests:
            {unit_tests[:500]}...
            
            Integration Tests:
            {integration_tests[:500]}...
            
            Provide:
            1. Test directory structure
            2. pytest.ini or pyproject.toml test configuration
            3. conftest.py with shared fixtures
            4. Test running instructions
            5. Coverage configuration
            6. CI/CD test pipeline suggestions
            """
            return claude_api_call(prompt)
    
    def _analyze_project_structure(self, path: Path) -> Dict[str, Any]:
        """Analyze project directory structure."""
        structure = {}
        
        if not path.exists():
            return structure
        
        try:
            for item in path.iterdir():
                if item.is_file() and item.suffix == '.py':
                    # Read Python file content
                    try:
                        content = item.read_text(encoding='utf-8')
                        structure[str(item)] = {
                            'type': 'file',
                            'content': content[:1000],  # First 1000 chars
                            'size': len(content),
                            'functions': self._extract_functions(content),
                            'classes': self._extract_classes(content)
                        }
                    except Exception as e:
                        structure[str(item)] = {'type': 'file', 'error': str(e)}
                        
                elif item.is_dir() and not item.name.startswith('.'):
                    # Recursively analyze subdirectories (limit depth)
                    structure[str(item)] = {
                        'type': 'directory',
                        'contents': self._analyze_project_structure(item)
                    }
        except PermissionError:
            structure['error'] = 'Permission denied'
        
        return structure
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names from Python code."""
        import re
        functions = re.findall(r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE)
        return functions
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names from Python code."""
        import re
        classes = re.findall(r'^class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE)
        return classes
    
    def _summarize_structure(self) -> str:
        """Create a readable summary of project structure."""
        summary = []
        
        def summarize_item(name, item, indent=0):
            prefix = "  " * indent
            if item.get('type') == 'file':
                functions = item.get('functions', [])
                classes = item.get('classes', [])
                summary.append(f"{prefix}{name} - {len(functions)} functions, {len(classes)} classes")
            elif item.get('type') == 'directory':
                summary.append(f"{prefix}{name}/")
                for subname, subitem in item.get('contents', {}).items():
                    summarize_item(subname, subitem, indent + 1)
        
        for name, item in self.project_structure.items():
            summarize_item(name, item)
        
        return '\n'.join(summary[:20])  # Limit output
    
    def _format_structure_for_analysis(self) -> str:
        """Format project structure for Claude analysis."""
        formatted = []
        
        def format_item(name, item, indent=0):
            prefix = "  " * indent
            if item.get('type') == 'file' and name.endswith('.py'):
                functions = item.get('functions', [])
                classes = item.get('classes', [])
                formatted.append(f"{prefix}{name}:")
                if classes:
                    formatted.append(f"{prefix}  Classes: {', '.join(classes)}")
                if functions:
                    formatted.append(f"{prefix}  Functions: {', '.join(functions)}")
                # Add snippet of content
                content = item.get('content', '')
                if content:
                    formatted.append(f"{prefix}  Content preview:")
                    for line in content.split('\n')[:5]:
                        formatted.append(f"{prefix}    {line}")
        
        for name, item in self.project_structure.items():
            format_item(name, item)
        
        return '\n'.join(formatted[:100])  # Limit output


def test_suite_writer(project_path: str = ".") -> str:
    """
    Convenience function to generate test suite for a project.
    
    Args:
        project_path: Path to project directory
        
    Returns:
        Complete test suite with organization
    """
    agent = TestSuiteWriterAgent(project_path)
    result = agent.agent_loop({"project_path": project_path})
    return result.content


def system_design_agent(requirement: str) -> str:
    """
    Convenience function to generate system design.
    
    Args:
        requirement: System requirement description
        
    Returns:
        System design with architecture and diagrams
    """
    agent = SystemDesignAgent()
    result = agent.agent_loop({"requirement": requirement})
    return result.content
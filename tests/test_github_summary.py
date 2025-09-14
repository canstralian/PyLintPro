"""Tests for GitHub summary generation functionality."""

import pytest
import tempfile
import json
from datetime import datetime
from scripts.github_summary import GitHubSummaryGenerator


class TestGitHubSummaryGenerator:
    """Test the GitHub summary generator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = GitHubSummaryGenerator("canstralian", "PyLintPro")
    
    def test_sample_commits_format(self):
        """Test that sample commits have the correct format."""
        commits = self.generator._get_sample_commits()
        
        assert len(commits) > 0
        for commit in commits:
            assert 'sha' in commit
            assert 'commit' in commit
            assert 'message' in commit['commit']
            assert 'author' in commit['commit']
            assert 'name' in commit['commit']['author']
            assert 'date' in commit['commit']['author']
    
    def test_sample_issues_format(self):
        """Test that sample issues have the correct format."""
        issues = self.generator._get_sample_issues()
        
        assert len(issues) > 0
        for issue in issues:
            assert 'number' in issue
            assert 'title' in issue
            assert 'user' in issue
            assert 'login' in issue['user']
            assert 'created_at' in issue
    
    def test_format_commit_summary(self):
        """Test commit summary formatting."""
        commits = self.generator._get_sample_commits()
        summary = self.generator.format_commit_summary(commits)
        
        assert "Yesterday's Commits" in summary
        assert str(len(commits)) in summary
        for commit in commits:
            assert commit['sha'][:7] in summary
            assert commit['commit']['author']['name'] in summary
    
    def test_format_issues_summary(self):
        """Test issues summary formatting."""
        issues = self.generator._get_sample_issues()
        summary = self.generator.format_issues_summary(issues)
        
        assert "Open Issues" in summary
        assert str(len(issues)) in summary
        for issue in issues:
            assert f"#{issue['number']}" in summary
            assert issue['title'] in summary
            assert issue['user']['login'] in summary
    
    def test_generate_complete_summary(self):
        """Test complete summary generation."""
        summary = self.generator.generate_summary()
        
        assert "GitHub Summary" in summary
        assert "canstralian/PyLintPro" in summary
        assert "Yesterday's Commits" in summary
        assert "Open Issues" in summary
        assert "Total Activity" in summary
    
    def test_empty_commits_handling(self):
        """Test handling of empty commits list."""
        summary = self.generator.format_commit_summary([])
        assert "No commits found" in summary
    
    def test_empty_issues_handling(self):
        """Test handling of empty issues list."""
        summary = self.generator.format_issues_summary([])
        assert "No open issues found" in summary


def test_github_summary_cli_integration():
    """Test CLI integration by running the script."""
    import subprocess
    import sys
    import os
    
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "github_summary.py")
    
    # Test help command
    result = subprocess.run(
        [sys.executable, script_path, "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Generate a summary" in result.stdout
    
    # Test normal execution
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "GitHub Summary" in result.stdout
    
    # Test JSON format
    result = subprocess.run(
        [sys.executable, script_path, "--format", "json"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    
    # Verify JSON output is valid
    output_data = json.loads(result.stdout)
    assert "repository" in output_data
    assert "commits" in output_data
    assert "issues" in output_data
    assert output_data["repository"] == "canstralian/PyLintPro"


def test_github_summary_output_file():
    """Test output to file functionality."""
    import subprocess
    import sys
    import os
    
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "github_summary.py")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as temp_file:
        temp_path = temp_file.name
    
    try:
        # Test output to file
        result = subprocess.run(
            [sys.executable, script_path, "--output", temp_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert f"Summary saved to: {temp_path}" in result.stdout
        
        # Verify file content
        with open(temp_path, 'r') as f:
            content = f.read()
        assert "GitHub Summary" in content
        assert "canstralian/PyLintPro" in content
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
#!/usr/bin/env python3
"""
GitHub Summary Generator for PyLintPro

Generates a summary of yesterday's commits and current open issues
for a GitHub repository. Falls back to sample data when API is not accessible.
"""

import argparse
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import os


class GitHubSummaryGenerator:
    """Generates summaries of GitHub repository activity."""
    
    def __init__(self, owner: str, repo: str, token: Optional[str] = None):
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PyLintPro-Summary-Generator"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def get_yesterday_commits(self) -> List[Dict[str, Any]]:
        """Fetch commits from yesterday."""
        yesterday = datetime.now() - timedelta(days=1)
        since_date = yesterday.strftime("%Y-%m-%dT00:00:00Z")
        until_date = yesterday.strftime("%Y-%m-%dT23:59:59Z")
        
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/commits"
        params = {
            "since": since_date,
            "until": until_date,
            "per_page": 100
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.warning(f"GitHub API not accessible ({e}), using sample data")
            return self._get_sample_commits()
    
    def _get_sample_commits(self) -> List[Dict[str, Any]]:
        """Return sample commits data for demonstration."""
        return [
            {
                "sha": "ff80f85fc3270fd79c0b5d82a706c45914319725",
                "commit": {
                    "message": "Merge pull request #34 from canstralian/copilot/fix-d5079818-2214-44ee-a013-c0e133c65f66\n\nImplement @ccxtpro_streamer decorator for cryptocurrency streaming functionality",
                    "author": {
                        "name": "WhacktheJacker",
                        "date": "2025-09-12T15:57:22Z"
                    }
                }
            },
            {
                "sha": "2c28482fce1bb9f5975de5bd5f1497fda8bedb66",
                "commit": {
                    "message": "Update demo_ccxtpro_streamer.py\n\nCo-authored-by: Copilot",
                    "author": {
                        "name": "WhacktheJacker",
                        "date": "2025-09-12T15:56:48Z"
                    }
                }
            }
        ]
    
    def get_open_issues(self) -> List[Dict[str, Any]]:
        """Fetch currently open issues."""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
        params = {
            "state": "open",
            "per_page": 100
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            # Filter out pull requests (they appear in issues API)
            issues = [issue for issue in response.json() if 'pull_request' not in issue]
            return issues
        except requests.RequestException as e:
            logging.warning(f"GitHub API not accessible ({e}), using sample data")
            return self._get_sample_issues()
    
    def _get_sample_issues(self) -> List[Dict[str, Any]]:
        """Return sample issues data for demonstration."""
        return [
            {
                "number": 37,
                "title": "Feature Request: Add Support for Custom Project Tags",
                "user": {"login": "tugascrown204"},
                "created_at": "2025-09-06T18:58:57Z",
                "labels": [],
                "body": "## Overview\n\nIt would be beneficial to enhance the project management features..."
            }
        ]
    
    def format_commit_summary(self, commits: List[Dict[str, Any]]) -> str:
        """Format commits into a readable summary."""
        if not commits:
            return "No commits found for yesterday."
        
        summary = [f"📝 **Yesterday's Commits ({len(commits)} total):**\n"]
        
        for commit in commits:
            sha = commit['sha'][:7]
            message = commit['commit']['message'].split('\n')[0]  # First line only
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            
            # Parse and format date
            commit_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            formatted_date = commit_date.strftime("%H:%M")
            
            summary.append(f"- **{sha}** - {message}")
            summary.append(f"  *by {author} at {formatted_date}*\n")
        
        return "\n".join(summary)
    
    def format_issues_summary(self, issues: List[Dict[str, Any]]) -> str:
        """Format issues into a readable summary."""
        if not issues:
            return "No open issues found."
        
        summary = [f"🐛 **Open Issues ({len(issues)} total):**\n"]
        
        for issue in issues:
            number = issue['number']
            title = issue['title']
            author = issue['user']['login']
            created_date = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
            days_ago = (datetime.now(created_date.tzinfo) - created_date).days
            
            # Add labels if any
            labels = issue.get('labels', [])
            label_text = ""
            if labels:
                label_names = [f"`{label['name']}`" for label in labels]
                label_text = f" [{', '.join(label_names)}]"
            
            summary.append(f"- **#{number}** - {title}{label_text}")
            summary.append(f"  *opened by {author}, {days_ago} days ago*\n")
        
        return "\n".join(summary)
    
    def generate_summary(self) -> str:
        """Generate a complete summary of yesterday's commits and open issues."""
        logging.info(f"Generating summary for {self.owner}/{self.repo}")
        
        # Fetch data
        commits = self.get_yesterday_commits()
        issues = self.get_open_issues()
        
        # Generate summary
        summary_parts = [
            f"# 📊 GitHub Summary for {self.owner}/{self.repo}",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')}*\n",
            "---\n",
            self.format_commit_summary(commits),
            "\n---\n",
            self.format_issues_summary(issues),
            "\n---\n",
            f"**Total Activity:** {len(commits)} commits yesterday, {len(issues)} open issues"
        ]
        
        return "\n".join(summary_parts)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a summary of yesterday's commits and open issues for a GitHub repository"
    )
    parser.add_argument(
        "--owner", 
        default="canstralian",
        help="Repository owner (default: canstralian)"
    )
    parser.add_argument(
        "--repo", 
        default="PyLintPro",
        help="Repository name (default: PyLintPro)"
    )
    parser.add_argument(
        "--token",
        help="GitHub API token (optional, but recommended for higher rate limits)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (if not provided, prints to stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Generate summary
    generator = GitHubSummaryGenerator(args.owner, args.repo, args.token)
    
    if args.format == "json":
        # JSON format for programmatic use
        commits = generator.get_yesterday_commits()
        issues = generator.get_open_issues()
        summary_data = {
            "repository": f"{args.owner}/{args.repo}",
            "generated_at": datetime.now().isoformat(),
            "yesterday_commits": len(commits),
            "open_issues": len(issues),
            "commits": commits,
            "issues": issues
        }
        output = json.dumps(summary_data, indent=2)
    else:
        # Markdown format for human reading
        output = generator.generate_summary()
    
    # Output results
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Summary saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
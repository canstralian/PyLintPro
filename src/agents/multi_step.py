# src/agents/multi_step.py

"""
Multi-step reasoning agents with complex workflows.
"""

import json
import subprocess
from typing import Any, Dict, List, Union
from .core import BaseAgent, AgentContext, claude_api_call


class CodeReviewerAgent(BaseAgent):
    """
    Automated code reviewer that analyzes git diffs and provides structured feedback.
    
    This agent performs multi-step analysis:
    1. Perceive: Extract git diff or code changes
    2. Reason: Plan review approach 
    3. Act: Generate structured review
    """
    
    def __init__(self):
        super().__init__(name="CodeReviewer", max_steps=3)
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Extract code changes to review."""
        if isinstance(input_data, dict):
            if "git_diff" in input_data:
                diff = input_data["git_diff"]
            elif "code_before" in input_data and "code_after" in input_data:
                diff = f"--- Before\n{input_data['code_before']}\n+++ After\n{input_data['code_after']}"
            else:
                diff = input_data.get("code", "")
        else:
            # Try to get git diff automatically
            diff = self._get_git_diff()
            if not diff:
                diff = str(input_data)
        
        self._current_diff = diff
        return f"Code changes to review:\n{diff}"
    
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """Plan the code review approach."""
        step = len(context)
        
        if step == 0:
            return "Analyze code changes for:\n" \
                   "1. Code quality and style issues\n" \
                   "2. Potential bugs or logic errors\n" \
                   "3. Security concerns\n" \
                   "4. Performance implications\n" \
                   "5. Test coverage needs"
        elif step == 1:
            return "Generate structured review with:\n" \
                   "1. Overall summary\n" \
                   "2. Major issues (critical fixes needed)\n" \
                   "3. Minor issues (improvements)\n" \
                   "4. Positive feedback (good practices)"
        else:
            return "Finalize review and format as JSON"
    
    def act(self, action_plan: str) -> Any:
        """Execute the review step."""
        step = len(getattr(self, '_context_history', []))
        
        if step == 0:
            # Initial analysis
            prompt = f"""
            You are an expert code reviewer. Analyze this code diff and identify issues:
            
            {self._current_diff}
            
            Focus on:
            - Code quality and style
            - Potential bugs
            - Security issues  
            - Performance concerns
            - Missing tests
            
            Provide a detailed analysis.
            """
            return claude_api_call(prompt)
            
        elif step == 1:
            # Structure the review
            analysis = getattr(self, '_previous_result', '')
            prompt = f"""
            Based on this code analysis:
            {analysis}
            
            Generate a structured code review in JSON format:
            {{
                "overall_summary": "Brief summary of changes and overall quality",
                "major_issues": ["List of critical issues that must be fixed"],
                "minor_issues": ["List of improvements and style suggestions"],
                "positive_feedback": ["Good practices and well-written parts"],
                "security_concerns": ["Any security-related issues"],
                "performance_notes": ["Performance implications"],
                "test_recommendations": ["Testing suggestions"]
            }}
            """
            return claude_api_call(prompt)
        
        else:
            # Return the structured result
            return getattr(self, '_structured_review', {})
    
    def _get_git_diff(self) -> str:
        """Get git diff for the current repository."""
        try:
            result = subprocess.run(
                ['git', 'diff', 'HEAD~1'], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            return result.stdout
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
            return ""
    
    def format_final_result(self, context: List[AgentContext]) -> str:
        """Format the final review result."""
        if len(context) >= 2:
            try:
                # Try to parse JSON from the structured review
                review_text = context[1].result
                # Extract JSON if it's embedded in text
                start = review_text.find('{')
                end = review_text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = review_text[start:end]
                    review = json.loads(json_str)
                    return self._format_review_output(review)
            except (json.JSONDecodeError, IndexError):
                pass
        
        # Fallback to text format
        return context[-1].result if context else "No review generated"
    
    def _format_review_output(self, review: Dict[str, Any]) -> str:
        """Format review dictionary as readable text."""
        output = []
        output.append("# Code Review Summary")
        output.append(f"\n## Overall Summary\n{review.get('overall_summary', 'N/A')}")
        
        if review.get('major_issues'):
            output.append("\n## Major Issues")
            for issue in review['major_issues']:
                output.append(f"- {issue}")
        
        if review.get('minor_issues'):
            output.append("\n## Minor Issues & Improvements")
            for issue in review['minor_issues']:
                output.append(f"- {issue}")
        
        if review.get('positive_feedback'):
            output.append("\n## Positive Feedback")
            for feedback in review['positive_feedback']:
                output.append(f"- {feedback}")
        
        return "\n".join(output)


class ResearchReportAgent(BaseAgent):
    """
    Agent that researches topics and generates comprehensive reports.
    
    Multi-step workflow:
    1. Plan research sources
    2. Collect information 
    3. Synthesize findings
    4. Generate report
    """
    
    def __init__(self):
        super().__init__(name="ResearchReport", max_steps=4)
        self._sources = []
        self._collected_data = ""
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Extract research query and parameters."""
        if isinstance(input_data, dict):
            query = input_data.get("query", "")
            sources = input_data.get("sources", [])
        else:
            query = str(input_data)
            sources = []
        
        self._research_query = query
        self._suggested_sources = sources
        
        return f"Research query: {query}"
    
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """Plan the research approach based on current step."""
        step = len(context)
        
        if step == 0:
            return "Plan research strategy:\n" \
                   "1. Identify key information sources\n" \
                   "2. Determine search keywords\n" \
                   "3. Plan information collection approach"
        elif step == 1:
            return "Collect information from identified sources"
        elif step == 2:
            return "Analyze and synthesize collected information"
        else:
            return "Generate comprehensive research report"
    
    def act(self, action_plan: str) -> str:
        """Execute research step."""
        step = len(getattr(self, '_context_history', []))
        
        if step == 0:
            # Plan research sources
            prompt = f"""
            Plan a research strategy for the query: "{self._research_query}"
            
            Suggest:
            1. Key information sources to consult
            2. Search keywords and terms
            3. Types of information to gather
            4. Research methodology
            
            Provide a structured research plan.
            """
            return claude_api_call(prompt)
            
        elif step == 1:
            # Simulate information collection
            self._collected_data = self._collect_information()
            return f"Collected information from {len(self._sources)} sources"
            
        elif step == 2:
            # Analyze information
            prompt = f"""
            Analyze this collected research data for the query "{self._research_query}":
            
            {self._collected_data}
            
            Identify:
            1. Key findings and insights
            2. Important trends or patterns
            3. Conflicting information or gaps
            4. Conclusions that can be drawn
            """
            return claude_api_call(prompt)
        
        else:
            # Generate final report
            analysis = context[2].result if len(context) > 2 else ""
            prompt = f"""
            Write a comprehensive research report on "{self._research_query}"
            
            Based on this analysis:
            {analysis}
            
            Structure the report with:
            1. Executive Summary
            2. Background/Context
            3. Key Findings
            4. Analysis and Insights
            5. Conclusions and Recommendations
            6. Sources and References
            
            Make it professional and well-organized.
            """
            return claude_api_call(prompt)
    
    def _collect_information(self) -> str:
        """
        Simulate information collection from various sources.
        
        In a real implementation, this would:
        - Search web sources
        - Read documentation
        - Query databases
        - Scrape relevant websites
        """
        # Placeholder implementation
        sources_info = [
            f"Source 1: Information about {self._research_query} from documentation",
            f"Source 2: Best practices related to {self._research_query}",
            f"Source 3: Recent developments in {self._research_query}",
        ]
        
        self._sources = ["Documentation", "Best Practices Guide", "Recent Articles"]
        return "\n\n".join(sources_info)


def code_review_agent() -> Dict[str, Any]:
    """
    Convenience function to run automated code review.
    
    Returns:
        Structured review results
    """
    agent = CodeReviewerAgent()
    result = agent.agent_loop({})
    
    # Try to parse as JSON, fallback to text
    try:
        if result.success and result.content:
            # Look for JSON in the result
            start = result.content.find('{')
            end = result.content.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(result.content[start:end])
    except json.JSONDecodeError:
        pass
    
    return {
        "overall_summary": result.content,
        "major_issues": [],
        "minor_issues": [],
        "positive_feedback": []
    }


def research_report_agent(query: str) -> str:
    """
    Convenience function to generate research report.
    
    Args:
        query: Research topic/question
        
    Returns:
        Comprehensive research report
    """
    agent = ResearchReportAgent()
    result = agent.agent_loop({"query": query})
    return result.content
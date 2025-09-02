# src/agents/api.py

"""
API integration for Claude agents with FastAPI backend.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel
from .core import BaseAgent, AgentResult
from .simple import explain_code, debug_error
from .multi_step import code_review_agent, research_report_agent
from .advanced import system_design_agent, test_suite_writer
from .meta import orchestrate_task


class AgentRequest(BaseModel):
    """Request model for agent API calls."""
    agent_type: str
    input_data: Dict[str, Any]
    max_steps: Optional[int] = 5


class AgentResponse(BaseModel):
    """Response model for agent API calls."""
    success: bool
    content: str
    agent_type: str
    steps_taken: int
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class AgentRegistry:
    """Registry of available agents and their functions."""
    
    @staticmethod
    def get_available_agents() -> Dict[str, str]:
        """Get list of available agents with descriptions."""
        return {
            "code_explainer": "Explains code functionality in detail",
            "fix_error": "Debugs and fixes code errors", 
            "code_reviewer": "Reviews code for quality, bugs, and security",
            "research_report": "Researches topics and generates reports",
            "system_design": "Creates system architecture and design",
            "test_suite_writer": "Generates comprehensive test suites",
            "meta_agent": "Orchestrates multiple agents for complex tasks"
        }
    
    @staticmethod
    def run_agent(agent_type: str, input_data: Dict[str, Any], max_steps: int = 5) -> AgentResponse:
        """
        Run a specific agent with given input.
        
        Args:
            agent_type: Type of agent to run
            input_data: Input data for the agent
            max_steps: Maximum execution steps
            
        Returns:
            AgentResponse with results
        """
        try:
            if agent_type == "code_explainer":
                code = input_data.get("code", "")
                language = input_data.get("language", "Python")
                result = explain_code(code, language)
                return AgentResponse(
                    success=True,
                    content=result,
                    agent_type=agent_type,
                    steps_taken=1
                )
                
            elif agent_type == "fix_error":
                code = input_data.get("code", "")
                error = input_data.get("error", "")
                result = debug_error(code, error)
                return AgentResponse(
                    success=True,
                    content=result,
                    agent_type=agent_type,
                    steps_taken=1
                )
                
            elif agent_type == "code_reviewer":
                result = code_review_agent()
                return AgentResponse(
                    success=True,
                    content=str(result),
                    agent_type=agent_type,
                    steps_taken=3,
                    metadata=result if isinstance(result, dict) else {}
                )
                
            elif agent_type == "research_report":
                query = input_data.get("query", input_data.get("topic", ""))
                result = research_report_agent(query)
                return AgentResponse(
                    success=True,
                    content=result,
                    agent_type=agent_type,
                    steps_taken=4
                )
                
            elif agent_type == "system_design":
                requirement = input_data.get("requirement", input_data.get("task", ""))
                result = system_design_agent(requirement)
                return AgentResponse(
                    success=True,
                    content=result,
                    agent_type=agent_type,
                    steps_taken=5
                )
                
            elif agent_type == "test_suite_writer":
                project_path = input_data.get("project_path", ".")
                result = test_suite_writer(project_path)
                return AgentResponse(
                    success=True,
                    content=result,
                    agent_type=agent_type,
                    steps_taken=4
                )
                
            elif agent_type == "meta_agent":
                task = input_data.get("task", "")
                task_type = input_data.get("type", "auto")
                context = input_data.get("context", {})
                result = orchestrate_task(task, task_type, context)
                return AgentResponse(
                    success=True,
                    content=result,
                    agent_type=agent_type,
                    steps_taken=6
                )
                
            else:
                return AgentResponse(
                    success=False,
                    content="",
                    agent_type=agent_type,
                    steps_taken=0,
                    error=f"Unknown agent type: {agent_type}"
                )
                
        except Exception as e:
            return AgentResponse(
                success=False,
                content="",
                agent_type=agent_type,
                steps_taken=0,
                error=str(e)
            )


# Convenience functions for common use cases
def quick_explain(code: str, language: str = "Python") -> str:
    """Quick code explanation."""
    response = AgentRegistry.run_agent("code_explainer", {"code": code, "language": language})
    return response.content if response.success else f"Error: {response.error}"


def quick_debug(code: str, error: str = "") -> str:
    """Quick error debugging."""
    response = AgentRegistry.run_agent("fix_error", {"code": code, "error": error})
    return response.content if response.success else f"Error: {response.error}"


def quick_review(code: str = "") -> str:
    """Quick code review."""
    response = AgentRegistry.run_agent("code_reviewer", {"code": code})
    return response.content if response.success else f"Error: {response.error}"


def quick_orchestrate(task: str, context: Dict[str, Any] = None) -> str:
    """Quick task orchestration."""
    input_data = {"task": task}
    if context:
        input_data["context"] = context
    response = AgentRegistry.run_agent("meta_agent", input_data)
    return response.content if response.success else f"Error: {response.error}"
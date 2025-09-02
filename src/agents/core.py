# src/agents/core.py

"""
Core agent framework implementing the Perceive → Reason → Act → Repeat pattern.
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """Context for agent execution, maintaining state across steps."""
    perception: str = ""
    action_plan: str = ""
    result: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Result of agent execution."""
    success: bool
    content: str
    context: List[AgentContext]
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all Claude-based agents.
    
    Implements the core Perceive → Reason → Act → Repeat pattern.
    """
    
    def __init__(self, name: str, max_steps: int = 5):
        self.name = name
        self.max_steps = max_steps
        self.logger = logging.getLogger(f"agent.{name}")
    
    def agent_loop(self, input_data: Union[str, Dict[str, Any]]) -> AgentResult:
        """
        Main agent loop implementing Perceive → Reason → Act → Repeat.
        
        Args:
            input_data: Initial input for the agent
            
        Returns:
            AgentResult containing the final result and execution context
        """
        context_history = []
        
        try:
            for step in range(self.max_steps):
                self.logger.info(f"Agent {self.name} - Step {step + 1}/{self.max_steps}")
                
                # Perceive
                perception = self.perceive(input_data, context_history)
                self.logger.debug(f"Perception: {perception[:100]}...")
                
                # Reason
                action_plan = self.reason(perception, context_history)
                self.logger.debug(f"Action plan: {action_plan[:100]}...")
                
                # Act
                result = self.act(action_plan)
                self.logger.debug(f"Result: {str(result)[:100]}...")
                
                # Update context
                context = AgentContext(
                    perception=perception,
                    action_plan=action_plan,
                    result=str(result)
                )
                context_history.append(context)
                
                # Check if task is complete
                if self.is_task_complete(result, context_history):
                    self.logger.info(f"Task completed in {step + 1} steps")
                    break
            
            return AgentResult(
                success=True,
                content=self.format_final_result(context_history),
                context=context_history
            )
            
        except Exception as e:
            self.logger.error(f"Agent {self.name} failed: {e}", exc_info=True)
            return AgentResult(
                success=False,
                content="",
                context=context_history,
                error=str(e)
            )
    
    @abstractmethod
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """
        Perceive the current state and input.
        
        Args:
            input_data: Current input data
            context: Previous execution context
            
        Returns:
            Perception string describing current state
        """
        pass
    
    @abstractmethod
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """
        Reason about the perception and plan actions.
        
        Args:
            perception: Current perception
            context: Previous execution context
            
        Returns:
            Action plan as a string
        """
        pass
    
    @abstractmethod
    def act(self, action_plan: str) -> Any:
        """
        Execute the action plan.
        
        Args:
            action_plan: Plan to execute
            
        Returns:
            Result of the action
        """
        pass
    
    def is_task_complete(self, result: Any, context: List[AgentContext]) -> bool:
        """
        Check if the task is complete.
        
        Args:
            result: Latest result
            context: Execution context
            
        Returns:
            True if task is complete
        """
        # Default implementation - can be overridden
        return len(context) >= self.max_steps
    
    def format_final_result(self, context: List[AgentContext]) -> str:
        """
        Format the final result from execution context.
        
        Args:
            context: Complete execution context
            
        Returns:
            Formatted final result
        """
        if not context:
            return "No results generated"
        
        return context[-1].result


def claude_api_call(prompt: str, system_prompt: str = "") -> str:
    """
    Placeholder for Claude API call.
    
    In a real implementation, this would call the Claude API.
    For now, returns a placeholder response.
    
    Args:
        prompt: User prompt for Claude
        system_prompt: System prompt (optional)
        
    Returns:
        Claude's response
    """
    # TODO: Implement actual Claude API integration
    # For now, return a placeholder
    return f"[Claude would respond to: {prompt[:50]}...]"


def agent_loop(input_data: Union[str, Dict[str, Any]], 
               agent_class: type, 
               max_steps: int = 5) -> AgentResult:
    """
    Convenience function to run an agent loop.
    
    Args:
        input_data: Input for the agent
        agent_class: Agent class to instantiate
        max_steps: Maximum steps to execute
        
    Returns:
        AgentResult from execution
    """
    agent = agent_class(name=agent_class.__name__, max_steps=max_steps)
    return agent.agent_loop(input_data)
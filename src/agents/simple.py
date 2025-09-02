# src/agents/simple.py

"""
Simple utility agents - stateless, single-purpose agents.
"""

from typing import Any, Dict, List, Union
from .core import BaseAgent, AgentContext, claude_api_call


class CodeExplainerAgent(BaseAgent):
    """
    Agent that explains code snippets in detail.
    
    This is a simple, stateless agent that takes code and returns
    a detailed explanation.
    """
    
    def __init__(self, language: str = "Python"):
        super().__init__(name="CodeExplainer", max_steps=1)
        self.language = language
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Extract code snippet from input."""
        if isinstance(input_data, dict):
            code = input_data.get("code", "")
            self.language = input_data.get("language", self.language)
        else:
            code = str(input_data)
        
        return f"Code to explain:\n```{self.language.lower()}\n{code}\n```"
    
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """Plan the explanation approach."""
        return f"Analyze and explain the {self.language} code in detail, covering:\n" \
               "1. What the code does (purpose/functionality)\n" \
               "2. How it works (step-by-step breakdown)\n" \
               "3. Key concepts and patterns used\n" \
               "4. Potential improvements or considerations"
    
    def act(self, action_plan: str) -> str:
        """Generate the code explanation using Claude."""
        # Extract code from previous perception
        if not hasattr(self, '_current_code'):
            return "No code provided to explain"
        
        prompt = f"""
        Explain the following {self.language} code in detail:
        
        ```{self.language.lower()}
        {self._current_code}
        ```
        
        Please provide:
        1. A clear explanation of what this code does
        2. Step-by-step breakdown of how it works
        3. Any important concepts or patterns used
        4. Suggestions for improvements if applicable
        """
        
        return claude_api_call(prompt)
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Extract code snippet from input and store it."""
        if isinstance(input_data, dict):
            code = input_data.get("code", "")
            self.language = input_data.get("language", self.language)
        else:
            code = str(input_data)
        
        self._current_code = code  # Store for later use
        return f"Code to explain:\n```{self.language.lower()}\n{code}\n```"


class FixErrorAgent(BaseAgent):
    """
    Agent that analyzes code errors and provides fixes.
    
    Takes code and error message, returns corrected code with explanation.
    """
    
    def __init__(self):
        super().__init__(name="FixError", max_steps=1)
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Extract code and error information."""
        if isinstance(input_data, dict):
            code = input_data.get("code", "")
            error = input_data.get("error", "")
        else:
            # Assume input is just code, no error provided
            code = str(input_data)
            error = "No specific error provided"
        
        self._current_code = code
        self._current_error = error
        
        return f"Code with error:\n```python\n{code}\n```\n\nError:\n{error}"
    
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """Plan the debugging approach."""
        return "Analyze the code and error to:\n" \
               "1. Identify the root cause of the error\n" \
               "2. Provide a corrected version of the code\n" \
               "3. Explain what went wrong and why\n" \
               "4. Suggest best practices to avoid similar issues"
    
    def act(self, action_plan: str) -> str:
        """Generate the fix and explanation using Claude."""
        prompt = f"""
        Analyze the code and the error below. Provide a corrected version and explain what went wrong.

        Code:
        ```python
        {self._current_code}
        ```

        Error:
        ```
        {self._current_error}
        ```
        
        Please provide:
        1. The corrected code
        2. Explanation of what was wrong
        3. Why the fix works
        4. Tips to avoid similar errors in the future
        
        Format your response as:
        ## Corrected Code
        ```python
        [corrected code here]
        ```
        
        ## Explanation
        [explanation here]
        """
        
        return claude_api_call(prompt)


def explain_code(code_snippet: str, language: str = "Python") -> str:
    """
    Convenience function to explain code using CodeExplainerAgent.
    
    Args:
        code_snippet: Code to explain
        language: Programming language
        
    Returns:
        Detailed explanation of the code
    """
    agent = CodeExplainerAgent(language=language)
    result = agent.agent_loop({"code": code_snippet, "language": language})
    return result.content


def debug_error(code_snippet: str, error_msg: str = "") -> str:
    """
    Convenience function to debug errors using FixErrorAgent.
    
    Args:
        code_snippet: Code with error
        error_msg: Error message (optional)
        
    Returns:
        Fixed code with explanation
    """
    agent = FixErrorAgent()
    result = agent.agent_loop({"code": code_snippet, "error": error_msg})
    return result.content
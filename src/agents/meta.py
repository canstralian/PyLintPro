# src/agents/meta.py

"""
Meta-agent for orchestrating and delegating to specialized agents.
"""

import json
from enum import Enum
from typing import Any, Dict, List, Union, Type
from .core import BaseAgent, AgentContext, claude_api_call
from .simple import CodeExplainerAgent, FixErrorAgent
from .multi_step import CodeReviewerAgent, ResearchReportAgent
from .advanced import SystemDesignAgent, TestSuiteWriterAgent


class AgentType(Enum):
    """Available agent types for delegation."""
    CODE_EXPLAINER = "code_explainer"
    FIX_ERROR = "fix_error"
    CODE_REVIEWER = "code_reviewer"
    RESEARCH_REPORT = "research_report"
    SYSTEM_DESIGN = "system_design"
    TEST_SUITE_WRITER = "test_suite_writer"


class MetaAgent(BaseAgent):
    """
    Meta-agent that orchestrates multiple specialized agents.
    
    This agent analyzes tasks and delegates to appropriate sub-agents,
    then coordinates their outputs to provide comprehensive results.
    """
    
    def __init__(self):
        super().__init__(name="MetaAgent", max_steps=6)
        self.agent_registry = {
            AgentType.CODE_EXPLAINER: CodeExplainerAgent,
            AgentType.FIX_ERROR: FixErrorAgent,
            AgentType.CODE_REVIEWER: CodeReviewerAgent,
            AgentType.RESEARCH_REPORT: ResearchReportAgent,
            AgentType.SYSTEM_DESIGN: SystemDesignAgent,
            AgentType.TEST_SUITE_WRITER: TestSuiteWriterAgent,
        }
        self.task_plan = {}
        self.sub_results = {}
    
    def perceive(self, input_data: Union[str, Dict[str, Any]], 
                 context: List[AgentContext]) -> str:
        """Analyze the task and understand requirements."""
        if isinstance(input_data, dict):
            task_description = input_data.get("task", "")
            task_type = input_data.get("type", "auto")
            additional_context = input_data.get("context", {})
        else:
            task_description = str(input_data)
            task_type = "auto"
            additional_context = {}
        
        self._task_description = task_description
        self._task_type = task_type
        self._additional_context = additional_context
        
        return f"Task to orchestrate: {task_description}"
    
    def reason(self, perception: str, context: List[AgentContext]) -> str:
        """Plan task decomposition and agent delegation."""
        step = len(context)
        
        if step == 0:
            return "Analyze task and determine:\n" \
                   "1. Task complexity and scope\n" \
                   "2. Which specialized agents are needed\n" \
                   "3. Order of execution and dependencies\n" \
                   "4. How to coordinate agent outputs"
        elif step == 1:
            return "Execute first phase of specialized agents"
        elif step == 2:
            return "Execute second phase and coordinate intermediate results"
        elif step == 3:
            return "Execute final phase and synthesize all results"
        else:
            return "Generate comprehensive final report"
    
    def act(self, action_plan: str) -> Any:
        """Execute orchestration step."""
        step = len(getattr(self, '_context_history', []))
        
        if step == 0:
            # Analyze and plan task decomposition
            return self._analyze_task()
        elif step == 1:
            # Execute first phase of agents
            return self._execute_agents_phase(1)
        elif step == 2:
            # Execute second phase
            return self._execute_agents_phase(2)
        elif step == 3:
            # Execute final phase
            return self._execute_agents_phase(3)
        else:
            # Synthesize final results
            return self._synthesize_results()
    
    def _analyze_task(self) -> str:
        """Analyze the task and create execution plan."""
        prompt = f"""
        Analyze this task and determine the best approach using available specialized agents:
        
        Task: {self._task_description}
        Type: {self._task_type}
        
        Available agents:
        - CodeExplainerAgent: Explains code functionality in detail
        - FixErrorAgent: Debugs and fixes code errors
        - CodeReviewerAgent: Reviews code for quality, bugs, security
        - ResearchReportAgent: Researches topics and generates reports
        - SystemDesignAgent: Creates system architecture and design
        - TestSuiteWriterAgent: Generates comprehensive test suites
        
        Determine:
        1. Which agents should be used
        2. In what order they should execute
        3. How their outputs should be combined
        4. What the final deliverable should be
        
        Respond with a JSON plan:
        {{
            "primary_agent": "agent_name",
            "supporting_agents": ["agent1", "agent2"],
            "execution_phases": [
                {{"phase": 1, "agents": ["agent1"], "description": "..."}},
                {{"phase": 2, "agents": ["agent2"], "description": "..."}}
            ],
            "final_synthesis": "description of how to combine results"
        }}
        """
        
        response = claude_api_call(prompt)
        
        # Try to extract JSON plan
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                self.task_plan = json.loads(response[start:end])
            else:
                # Fallback plan
                self.task_plan = self._create_fallback_plan()
        except json.JSONDecodeError:
            self.task_plan = self._create_fallback_plan()
        
        return f"Task analysis complete. Plan: {json.dumps(self.task_plan, indent=2)}"
    
    def _create_fallback_plan(self) -> Dict[str, Any]:
        """Create a fallback execution plan based on task keywords."""
        task_lower = self._task_description.lower()
        
        if any(word in task_lower for word in ["explain", "understand", "what does"]):
            return {
                "primary_agent": "code_explainer",
                "supporting_agents": [],
                "execution_phases": [
                    {"phase": 1, "agents": ["code_explainer"], "description": "Explain code"}
                ],
                "final_synthesis": "Return explanation directly"
            }
        elif any(word in task_lower for word in ["fix", "error", "bug", "debug"]):
            return {
                "primary_agent": "fix_error",
                "supporting_agents": ["code_reviewer"],
                "execution_phases": [
                    {"phase": 1, "agents": ["fix_error"], "description": "Fix the error"},
                    {"phase": 2, "agents": ["code_reviewer"], "description": "Review the fix"}
                ],
                "final_synthesis": "Combine fix with review feedback"
            }
        elif any(word in task_lower for word in ["review", "analyze", "quality"]):
            return {
                "primary_agent": "code_reviewer",
                "supporting_agents": [],
                "execution_phases": [
                    {"phase": 1, "agents": ["code_reviewer"], "description": "Review code"}
                ],
                "final_synthesis": "Return review directly"
            }
        else:
            # Default to code explanation
            return {
                "primary_agent": "code_explainer",
                "supporting_agents": [],
                "execution_phases": [
                    {"phase": 1, "agents": ["code_explainer"], "description": "Explain task"}
                ],
                "final_synthesis": "Return explanation directly"
            }
    
    def _execute_agents_phase(self, phase_num: int) -> str:
        """Execute agents for a specific phase."""
        phases = self.task_plan.get("execution_phases", [])
        current_phase = None
        
        for phase in phases:
            if phase.get("phase") == phase_num:
                current_phase = phase
                break
        
        if not current_phase:
            return f"No phase {phase_num} defined"
        
        agents_to_run = current_phase.get("agents", [])
        results = []
        
        for agent_name in agents_to_run:
            result = self._run_sub_agent(agent_name)
            self.sub_results[agent_name] = result
            results.append(f"{agent_name}: {result[:200]}...")
        
        return f"Phase {phase_num} complete. Results: {'; '.join(results)}"
    
    def _run_sub_agent(self, agent_name: str) -> str:
        """Run a specific sub-agent."""
        # Map agent names to enum values
        agent_mapping = {
            "code_explainer": AgentType.CODE_EXPLAINER,
            "fix_error": AgentType.FIX_ERROR,
            "code_reviewer": AgentType.CODE_REVIEWER,
            "research_report": AgentType.RESEARCH_REPORT,
            "system_design": AgentType.SYSTEM_DESIGN,
            "test_suite_writer": AgentType.TEST_SUITE_WRITER,
        }
        
        agent_type = agent_mapping.get(agent_name)
        if not agent_type or agent_type not in self.agent_registry:
            return f"Unknown agent: {agent_name}"
        
        try:
            # Create and run the agent
            agent_class = self.agent_registry[agent_type]
            
            if agent_type == AgentType.CODE_EXPLAINER:
                agent = agent_class()
            elif agent_type == AgentType.FIX_ERROR:
                agent = agent_class()
            elif agent_type == AgentType.CODE_REVIEWER:
                agent = agent_class()
            elif agent_type == AgentType.RESEARCH_REPORT:
                agent = agent_class()
            elif agent_type == AgentType.SYSTEM_DESIGN:
                agent = agent_class()
            elif agent_type == AgentType.TEST_SUITE_WRITER:
                agent = agent_class()
            else:
                return f"Unsupported agent type: {agent_type}"
            
            # Prepare input for the sub-agent
            sub_input = self._prepare_sub_agent_input(agent_name)
            
            # Run the agent
            result = agent.agent_loop(sub_input)
            
            return result.content if result.success else f"Error: {result.error}"
            
        except Exception as e:
            self.logger.error(f"Error running sub-agent {agent_name}: {e}")
            return f"Error running {agent_name}: {str(e)}"
    
    def _prepare_sub_agent_input(self, agent_name: str) -> Union[str, Dict[str, Any]]:
        """Prepare input for a specific sub-agent."""
        base_input = {
            "task": self._task_description,
            "context": self._additional_context
        }
        
        if agent_name == "code_explainer":
            return base_input.get("code", self._task_description)
        elif agent_name == "fix_error":
            return {
                "code": base_input.get("code", ""),
                "error": base_input.get("error", "")
            }
        elif agent_name == "code_reviewer":
            return base_input
        elif agent_name == "research_report":
            return {"query": self._task_description}
        elif agent_name == "system_design":
            return {"requirement": self._task_description}
        elif agent_name == "test_suite_writer":
            return {"project_path": base_input.get("project_path", ".")}
        else:
            return self._task_description
    
    def _synthesize_results(self) -> str:
        """Synthesize results from all sub-agents."""
        synthesis_plan = self.task_plan.get("final_synthesis", "Combine all results")
        
        prompt = f"""
        Synthesize these agent results into a comprehensive response:
        
        Original Task: {self._task_description}
        
        Agent Results:
        """
        
        for agent_name, result in self.sub_results.items():
            prompt += f"\n{agent_name}:\n{result}\n"
        
        prompt += f"""
        
        Synthesis Instructions: {synthesis_plan}
        
        Create a unified, comprehensive response that:
        1. Addresses the original task completely
        2. Integrates insights from all agents
        3. Provides actionable recommendations
        4. Is well-organized and professional
        """
        
        return claude_api_call(prompt)
    
    def format_final_result(self, context: List[AgentContext]) -> str:
        """Format the final orchestrated result."""
        if not context:
            return "No results generated"
        
        # Return the synthesized result
        return context[-1].result


def orchestrate_task(task_description: str, 
                    task_type: str = "auto",
                    context: Dict[str, Any] = None) -> str:
    """
    Convenience function to orchestrate a complex task using multiple agents.
    
    Args:
        task_description: Description of the task to accomplish
        task_type: Type of task (auto-detected if not specified)
        context: Additional context for the task
        
    Returns:
        Comprehensive result from orchestrated agents
    """
    meta_agent = MetaAgent()
    
    input_data = {
        "task": task_description,
        "type": task_type,
        "context": context or {}
    }
    
    result = meta_agent.agent_loop(input_data)
    return result.content
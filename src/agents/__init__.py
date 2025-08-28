# src/agents/__init__.py

"""
Claude-based code agent framework for PyLintPro.

This module provides a framework for implementing Claude-based agents with
increasing complexity, following the Perceive → Reason → Act → Repeat pattern.
"""

# Import core components first
from .core import BaseAgent, AgentContext, AgentResult

# Import agents conditionally to handle import errors gracefully
try:
    from .simple import CodeExplainerAgent, FixErrorAgent
except ImportError as e:
    print(f"Warning: Could not import simple agents: {e}")
    CodeExplainerAgent = None
    FixErrorAgent = None

try:
    from .multi_step import CodeReviewerAgent, ResearchReportAgent
except ImportError as e:
    print(f"Warning: Could not import multi-step agents: {e}")
    CodeReviewerAgent = None
    ResearchReportAgent = None

try:
    from .advanced import SystemDesignAgent, TestSuiteWriterAgent
except ImportError as e:
    print(f"Warning: Could not import advanced agents: {e}")
    SystemDesignAgent = None
    TestSuiteWriterAgent = None

try:
    from .meta import MetaAgent
except ImportError as e:
    print(f"Warning: Could not import meta agent: {e}")
    MetaAgent = None

# Export available components
__all__ = [
    "BaseAgent",
    "AgentContext", 
    "AgentResult",
]

# Add available agents to exports
if CodeExplainerAgent:
    __all__.extend(["CodeExplainerAgent", "FixErrorAgent"])
if CodeReviewerAgent:
    __all__.extend(["CodeReviewerAgent", "ResearchReportAgent"])
if SystemDesignAgent:
    __all__.extend(["SystemDesignAgent", "TestSuiteWriterAgent"])
if MetaAgent:
    __all__.append("MetaAgent")
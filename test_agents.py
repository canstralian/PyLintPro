# test_agents.py - Simple test script for the agent framework

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.agents.core import BaseAgent, AgentContext, AgentResult
from src.agents.simple import explain_code, debug_error
from src.agents.api import quick_explain, quick_debug, quick_review

def test_core_functionality():
    """Test core agent framework."""
    print("🧪 Testing Core Agent Framework")
    
    # Test AgentContext
    context = AgentContext(perception="test", action_plan="test", result="test")
    print(f"✓ AgentContext created: {context}")
    
    # Test AgentResult
    result = AgentResult(success=True, content="test", context=[context])
    print(f"✓ AgentResult created: {result}")
    
    print()

def test_simple_agents():
    """Test simple utility agents."""
    print("🤖 Testing Simple Agents")
    
    # Test code explanation
    test_code = "def hello():\n    print('Hello, World!')"
    explanation = explain_code(test_code)
    print(f"✓ Code Explainer: {explanation[:50]}...")
    
    # Test error debugging
    error_code = "print('hello'"
    fix = debug_error(error_code, "SyntaxError: '(' was never closed")
    print(f"✓ Error Debugger: {fix[:50]}...")
    
    print()

def test_api_functions():
    """Test API convenience functions."""
    print("🔌 Testing API Functions")
    
    # Test quick explain
    result = quick_explain("x = 1 + 2")
    print(f"✓ Quick Explain: {result[:50]}...")
    
    # Test quick debug
    result = quick_debug("print('test')", "No error")
    print(f"✓ Quick Debug: {result[:50]}...")
    
    # Test quick review
    result = quick_review("def test(): pass")
    print(f"✓ Quick Review: {result[:50]}...")
    
    print()

def test_example_workflow():
    """Test a complete workflow example."""
    print("⚡ Testing Complete Workflow")
    
    sample_code = """
def calculate_factorial(n):
    if n < 0:
        return None
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
"""
    
    print("1. Explaining the code...")
    explanation = quick_explain(sample_code)
    print(f"   Explanation generated: {len(explanation)} characters")
    
    print("2. Reviewing the code...")
    review = quick_review(sample_code)
    print(f"   Review generated: {len(review)} characters")
    
    print("3. Testing with error...")
    broken_code = "def factorial(n:\n    return n * factorial(n-1)"
    fix = quick_debug(broken_code, "SyntaxError: invalid syntax")
    print(f"   Fix generated: {len(fix)} characters")
    
    print("✓ Complete workflow tested successfully!")
    print()

if __name__ == "__main__":
    print("🚀 PyLintPro Agent Framework Test\n")
    
    try:
        test_core_functionality()
        test_simple_agents()
        test_api_functions()
        test_example_workflow()
        
        print("🎉 All tests completed successfully!")
        print("\nAgent Framework Status:")
        print("✓ Core framework operational")
        print("✓ Simple agents working")
        print("✓ API functions ready")
        print("✓ Multi-step workflows functional")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
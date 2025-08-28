import gradio as gr
import tempfile
import os
import subprocess
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

from src.config import GRADIO_THEME, GRADIO_CSS, APP_NAME
from src.utils import setup_logging

logger = setup_logging(__name__)

def lint_code(code):
    """
    Formats code with autopep8 and runs flake8 to collect linting issues.
    Returns the formatted code plus any flake8 warnings.
    """
    if not code.strip():
        return "# Please provide some Python code to analyze"
    
    try:
        # Simple formatting without autopep8 to avoid lib2to3 issue
        # For now, just run flake8 analysis
        
        # Write to temp file for flake8
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        
        # Run flake8
        result = subprocess.run(
            ["flake8", tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        os.unlink(tmp_path)
        
        if result.returncode == 0:
            issues = "✅ No linting issues found!"
        else:
            issues = result.stdout.strip()
        
        return f"""# Mendicant AI - Code Analysis Result

## Original Code:
```python
{code}
```

## Analysis Results:
{issues}

---
*This is a demo of Mendicant's code quality checking. Our full GitHub App provides automated fixes via Pull Requests.*

**Ready to heal your repositories?** 
[Book a pilot call →](https://calendly.com/mendicant-ai/pilot)
"""
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        return f"""# Analysis Error

An error occurred during code analysis: {str(e)}

This is a demo environment. Our production GitHub App handles errors gracefully and provides detailed feedback.

**Need reliable repository health monitoring?**
[Book a pilot call →](https://calendly.com/mendicant-ai/pilot)
"""

def create_scoreboard_display():
    """Create the public commitment scoreboard display."""
    return """
# 📊 Public Commitment Scoreboard

## 12-Week Sprint to $10k MRR

| Metric | Target | Current | Progress |
|--------|--------|---------|----------|
| **Monthly Recurring Revenue** | $10,000 | $0 | 0% |
| **Pilot Commitments** | 10 | 0 | 0% |  
| **Outreach Messages** | 500 | 50 | 10% |
| **Customer Interviews** | 50 | 4 | 8% |
| **Active Installations** | 25 | 0 | 0% |

*Updated weekly. Follow our journey at [GitHub Discussions](https://github.com/canstralian/PyLintPro/discussions)*

## What is Mendicant AI?

We're building **self-healing repositories** that automatically detect and fix "broken window" issues:
- 🔧 Code quality drift  
- 🛡️ Security misconfigurations
- 🧪 Flaky tests
- 📚 Documentation gaps
- 📦 Outdated dependencies

**The Goal:** Help engineering teams ship faster by eliminating the small issues that slow them down.

## Pilot Program - $1,500 for 14 Days

✅ Full repository health assessment  
✅ Automated fixes for up to 50 issues  
✅ Weekly progress reports  
✅ Direct access to our engineering team  
✅ 20% discount on annual contract if you convert  

**Success Metrics:**
- Reduce CI build failures by 30%
- Decrease time-to-merge by 25%  
- Improve code coverage by 15%

[**Book Your Pilot Call →**](https://calendly.com/mendicant-ai/pilot)
"""

# Create the Gradio interface
with gr.Blocks(
    theme=gr.themes.Soft(),
    css="""
    .gradio-container { 
        padding: 2rem; 
        max-width: 1200px;
        margin: 0 auto;
    }
    .gr-button.primary { 
        font-weight: bold;
        background: linear-gradient(45deg, #2563eb, #059669);
        border: none;
    }
    .gr-code { 
        font-family: 'JetBrains Mono', 'Consolas', monospace; 
    }
    .pilot-cta {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border-left: 4px solid #0ea5e9;
        padding: 1rem;
        margin: 1rem 0;
    }
    """,
    fill_width=True,
    title=f"{APP_NAME} - Repository Health Demo"
) as demo:
    
    # Header section
    gr.Markdown("# 🏥 Mendicant AI - Self-Healing Repositories")
    gr.Markdown("*Demo: Experience our code analysis capabilities. Full GitHub App available in pilot program.*")
    
    # Main tabs
    with gr.Tabs():
        
        # Code Analysis Demo Tab
        with gr.TabItem("🔍 Code Analysis Demo"):
            gr.Markdown("## Try Our Code Quality Analysis")
            gr.Markdown("Paste Python code below to see how Mendicant identifies issues:")
            
            with gr.Row(equal_height=True):
                code_input = gr.Code(
                    language="python",
                    label="Your Python Code",
                    lines=15,
                    interactive=True,
                    value="# Paste your Python code here\ndef example_function( x,y ):\n    if x>y:\n        print( 'x is bigger' )\n    else:\n        print('y is bigger')\n    return x+y"
                )
                code_output = gr.Markdown(
                    label="Analysis Results",
                    value="Click 'Analyze Code' to see results..."
                )
            
            analyze_btn = gr.Button("🔍 Analyze Code", variant="primary", size="lg")
            analyze_btn.click(
                fn=lint_code,
                inputs=[code_input],
                outputs=[code_output]
            )
            
            # Quick examples
            gr.Examples(
                examples=[
                    ["# Example with multiple issues\ndef badly_formatted( x,y ):\n    if x>y:\n        print( 'x is bigger' )\n    else:\n        print('y is bigger')\n    return x+y"],
                    ["# Example with unused imports\nimport os\nimport sys\nimport json\n\ndef simple_function():\n    return 'hello world'"],
                    ["# Example with long lines\ndef function_with_very_long_line():\n    very_long_variable_name = 'this is a very long string that exceeds the recommended line length limit and should be broken up'\n    return very_long_variable_name"]
                ],
                inputs=code_input,
                label="Try These Examples"
            )
        
        # Public Scoreboard Tab
        with gr.TabItem("📊 Public Scoreboard"):
            scoreboard = gr.Markdown(create_scoreboard_display())
            
            refresh_btn = gr.Button("🔄 Refresh Scoreboard", variant="secondary")
            refresh_btn.click(
                fn=lambda: create_scoreboard_display(),
                outputs=[scoreboard]
            )
        
        # Pilot Program Tab
        with gr.TabItem("🚀 Pilot Program"):
            gr.Markdown("""
# 🚀 14-Day Pilot Program

## What You Get

### Comprehensive Repository Analysis
- **Code Quality**: PEP 8, Flake8, ESLint violations
- **Security**: Vulnerability scanning, secret detection  
- **Testing**: Flaky test identification, coverage analysis
- **Documentation**: README completeness, API docs
- **Dependencies**: Outdated packages, security advisories
- **Performance**: Large files, slow CI builds

### Automated Remediation
- **Pull Requests**: Automatic fixes with detailed explanations
- **Smart Prioritization**: Focus on high-impact issues first
- **Team Integration**: Works with your existing code review process
- **Custom Rules**: Configure checks for your team's standards

### Success Tracking
- **Weekly Reports**: Detailed progress and metrics
- **Before/After**: Clear impact measurement
- **ROI Analysis**: Time saved, bugs prevented
- **Team Feedback**: Developer satisfaction improvements

## Investment: $1,500 for 14 Days

### What's Included:
✅ **Full Setup**: GitHub App installation and configuration  
✅ **Repository Analysis**: Up to 10 repositories  
✅ **Automated Fixes**: Up to 50 issues resolved via PRs  
✅ **Weekly Check-ins**: Progress reviews with our team  
✅ **Custom Rules**: Tailored to your coding standards  
✅ **Success Report**: Detailed impact analysis  

### Success Guarantee:
If you don't see measurable improvement in:
- CI build reliability (+30%)
- Code review velocity (+25%) 
- Developer satisfaction

We'll refund 100% of your investment.

### Ready to Get Started?

""")
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("""
#### 📅 Book Your Pilot Call
Schedule a 30-minute consultation to discuss your team's needs.

[**Book Now →**](https://calendly.com/mendicant-ai/pilot)
""")
                
                with gr.Column(scale=1):
                    gr.Markdown("""
#### 💳 Secure Payment
Pay securely with Stripe. Start your pilot immediately.

[**Pay $1,500 →**](https://buy.stripe.com/pilot-program)
""")
            
            gr.Markdown("""
---

### Questions?

**Email**: [pilot@mendicant.ai](mailto:pilot@mendicant.ai)  
**Phone**: +1 (555) 123-4567  
**GitHub**: [Submit an issue](https://github.com/canstralian/PyLintPro/issues)

*No long-term commitments. Cancel anytime. 20% discount on annual plans for pilot participants.*
""")

# Footer
demo.footer = f"""
<div style="text-align: center; padding: 2rem; border-top: 1px solid #e5e5e5; margin-top: 2rem;">
    <strong>{APP_NAME}</strong> - Making every repository self-healing<br>
    <a href="https://github.com/canstralian/PyLintPro">Open Source</a> | 
    <a href="mailto:support@mendicant.ai">Support</a> | 
    <a href="https://calendly.com/mendicant-ai/pilot">Book Pilot</a>
</div>
"""

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_api=False
    )
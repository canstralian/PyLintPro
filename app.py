import gradio as gr
import autopep8
import tempfile
import os
import subprocess


def lint_code(code):
    """
    Formats code with autopep8 and runs flake8 to collect linting issues.
    Returns the formatted code plus any flake8 warnings.
    """
    if not code or not code.strip():
        return "# No code provided for analysis"

    try:
        # Format with autopep8
        formatted_code = autopep8.fix_code(
            code, options={"aggressive": 1, "max_line_length": 88}
        )
        # Write to temp file for flake8
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".py", delete=False
        ) as tmp:
            tmp.write(formatted_code)
            tmp_path = tmp.name

        # Run flake8
        result = subprocess.run(
            ["flake8", tmp_path, "--max-line-length=88", "--ignore=E203,W503"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        os.unlink(tmp_path)
        issues = result.stdout.strip() or "✅ No issues found."
        return f"{formatted_code}\n\n# 🔍 Flake8 Analysis:\n# {issues}"

    except Exception as e:
        return f"# ❌ Error processing code: {str(e)}\n\n{code}"


# Iteration 1: Basic layout with two code editors
with gr.Blocks() as demo:
    with gr.Row(equal_height=True):
        code_input = gr.Code(
            language="python",
            label="Your Code",
            lines=20,
            interactive=True
        )
        code_output = gr.Code(
            language="python",
            label="Linted Code",
            lines=20,
            interactive=False
        )

    # Iteration 2: Add the lint button and wire the event
    lint_btn = gr.Button("Lint Code", variant="primary")
    lint_btn.click(
        fn=lint_code,
        inputs=[code_input],
        outputs=[code_output]
    )

    # Iteration 3: Add example snippets for quick testing
    gr.Examples(
        examples=[
            ["print( 'hello world' )"],
            ["def foo():\n    x=1\n    return x"],
            ["# Example with various PEP 8 issues\n"
             "def bad_function( x,y ):\n"
             "    result=x+y    # Missing spaces\n"
             "    return result\n\n"
             "class my_class:\n"
             "    def __init__(self):\n"
             "        pass"]
        ],
        inputs=code_input,
        label="Try These Snippets"
    )

# Iteration 4: Apply a theme, custom CSS, and full-width layout
demo.theme = gr.themes.Soft()
demo.css = """
.gradio-container { padding: 2rem; }
.gr-button.primary { font-weight: bold; }
.gr-code { font-family: 'JetBrains Mono', monospace; }
"""
demo.fill_width = True

# Iteration 5: Add progress indicator to the lint button
lint_btn.show_progress = "minimal"

if __name__ == "__main__":
    demo.launch()
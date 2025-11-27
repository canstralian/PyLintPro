import gradio as gr
from src.lint import lint_code


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
            ["def foo():\n    x=1\n    return x"]
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

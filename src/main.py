# src/main.py

import gradio as gr
from src.config import GRADIO_THEME, GRADIO_CSS  # Centralized UI settings
from src.lint import lint_code  # Business logic for formatting and linting


def main():
    # Build the Gradio Blocks application
    with gr.Blocks(
        theme=GRADIO_THEME,  # Apply a prebuilt Soft theme
        css=GRADIO_CSS,  # Inject custom CSS for padding and fonts
        fill_width=True  # Use full browser width for layout
    ) as demo:
        # Side-by-side input/output editors
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

        # Primary action button with progress indicator
        lint_btn = gr.Button("Lint Code", variant="primary")
        lint_btn.click(
            fn=lint_code,
            inputs=[code_input],
            outputs=[code_output],
            show_progress="minimal"
        )

        # Predefined examples to auto-fill the input editor
        gr.Examples(
            examples=[
                ["print( 'hello world' )"],
                ["def foo():\n    x=1\n    return x"]
            ],
            inputs=code_input
        )

    demo.launch()


if __name__ == "__main__":
    main()

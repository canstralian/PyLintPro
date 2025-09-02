# src/main.py

import gradio as gr
from src.config import GRADIO_THEME, GRADIO_CSS       # Centralized UI settings
from src.lint import lint_code                         # Business logic for formatting and linting

# Import agent functions (optional)
try:
    from src.agents.api import quick_explain, quick_debug, quick_review, quick_orchestrate
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    print("Agent framework not available - running in basic mode")


def main():
    # Build the Gradio Blocks application
    with gr.Blocks(
        theme=GRADIO_THEME,                            # Apply a prebuilt Soft theme
        css=GRADIO_CSS,                                 # Inject custom CSS for padding and fonts
        fill_width=True                                 # Use full browser width for layout
    ) as demo:
        
        gr.Markdown("# PyLintPro - Python Code Linting & AI Agents")
        
        # Create tabs for different functionalities
        with gr.Tabs():
            # Original linting tab
            with gr.TabItem("Code Linting"):
                gr.Markdown("### Lint and format your Python code")
                
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
            
            # Agent tabs (if available)
            if AGENTS_AVAILABLE:
                with gr.TabItem("Code Explainer"):
                    gr.Markdown("### Get detailed explanations of your code")
                    
                    with gr.Row():
                        with gr.Column(scale=1):
                            explain_code_input = gr.Code(
                                language="python",
                                label="Code to Explain",
                                lines=15,
                                interactive=True
                            )
                            explain_language = gr.Dropdown(
                                choices=["Python", "JavaScript", "Java", "C++", "C#"],
                                value="Python",
                                label="Language"
                            )
                            explain_btn = gr.Button("Explain Code", variant="primary")
                        
                        with gr.Column(scale=1):
                            explain_output = gr.Markdown(
                                label="Explanation",
                                value="Code explanation will appear here..."
                            )
                    
                    explain_btn.click(
                        fn=lambda code, lang: quick_explain(code, lang) if code.strip() else "Please provide code to explain",
                        inputs=[explain_code_input, explain_language],
                        outputs=[explain_output],
                        show_progress="minimal"
                    )
                    
                    gr.Examples(
                        examples=[
                            ["def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)", "Python"],
                            ["class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return f'{self.name} says woof!'", "Python"]
                        ],
                        inputs=[explain_code_input, explain_language]
                    )
                
                with gr.TabItem("Error Debugger"):
                    gr.Markdown("### Debug and fix code errors")
                    
                    with gr.Row():
                        with gr.Column():
                            debug_code_input = gr.Code(
                                language="python",
                                label="Code with Error",
                                lines=12,
                                interactive=True
                            )
                            debug_error_input = gr.Textbox(
                                label="Error Message (optional)",
                                lines=3,
                                placeholder="Paste error message here..."
                            )
                            debug_btn = gr.Button("Debug & Fix", variant="primary")
                        
                        with gr.Column():
                            debug_output = gr.Markdown(
                                label="Fix & Explanation",
                                value="Debug results will appear here..."
                            )
                    
                    debug_btn.click(
                        fn=lambda code, error: quick_debug(code, error) if code.strip() else "Please provide code to debug",
                        inputs=[debug_code_input, debug_error_input],
                        outputs=[debug_output],
                        show_progress="minimal"
                    )
                    
                    gr.Examples(
                        examples=[
                            ["print('Hello World'", "SyntaxError: '(' was never closed"],
                            ["def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)", "ZeroDivisionError: division by zero"]
                        ],
                        inputs=[debug_code_input, debug_error_input]
                    )
                
                with gr.TabItem("Code Reviewer"):
                    gr.Markdown("### Get automated code reviews")
                    
                    with gr.Row():
                        with gr.Column():
                            review_code_input = gr.Code(
                                language="python",
                                label="Code to Review",
                                lines=15,
                                interactive=True
                            )
                            review_btn = gr.Button("Review Code", variant="primary")
                        
                        with gr.Column():
                            review_output = gr.Markdown(
                                label="Code Review",
                                value="Code review will appear here..."
                            )
                    
                    review_btn.click(
                        fn=lambda code: quick_review(code) if code.strip() else "Please provide code to review",
                        inputs=[review_code_input],
                        outputs=[review_output],
                        show_progress="minimal"
                    )
                
                with gr.TabItem("AI Assistant"):
                    gr.Markdown("### General AI coding assistance")
                    
                    with gr.Row():
                        with gr.Column():
                            task_input = gr.Textbox(
                                label="Task Description",
                                lines=3,
                                placeholder="Describe what you want help with..."
                            )
                            context_input = gr.Code(
                                language="python",
                                label="Code Context (optional)",
                                lines=10,
                                interactive=True
                            )
                            assist_btn = gr.Button("Get Assistance", variant="primary")
                        
                        with gr.Column():
                            assist_output = gr.Markdown(
                                label="AI Response",
                                value="AI assistance will appear here..."
                            )
                    
                    def handle_assistance(task, context):
                        if not task.strip():
                            return "Please provide a task description"
                        
                        context_dict = {"code": context} if context.strip() else {}
                        return quick_orchestrate(task, context_dict)
                    
                    assist_btn.click(
                        fn=handle_assistance,
                        inputs=[task_input, context_input],
                        outputs=[assist_output],
                        show_progress="minimal"
                    )
                    
                    gr.Examples(
                        examples=[
                            ["Explain how to implement a binary search algorithm", ""],
                            ["Review this code for potential improvements", "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr"],
                            ["Generate unit tests for this function", "def calculate_average(numbers):\n    if not numbers:\n        return 0\n    return sum(numbers) / len(numbers)"]
                        ],
                        inputs=[task_input, context_input]
                    )
            
            else:
                with gr.TabItem("AI Agents"):
                    gr.Markdown("### AI Agent Framework")
                    gr.Markdown("⚠️ **Agent framework is not available.** Please ensure all dependencies are installed.")

    demo.launch()


if __name__ == "__main__":
    main()
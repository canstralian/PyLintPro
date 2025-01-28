# Import necessary libraries
import gradio as gr
from flake8.api import legacy as flake8
import autopep8

# Define a function to lint and fix Python code
def lint_code(code):
    # Run Flake8 for linting
    style_guide = flake8.get_style_guide(ignore=["E501"])  # Ignore line-length violations
    report = style_guide.check_files(None, lines=code.splitlines())
    
    # Auto-fix with autopep8
    fixed_code = autopep8.fix_code(code)
    return fixed_code, "\n".join(msg for msg in report.get_statistics())

# Define a function to process the uploaded file
def process_file(file):
    # Read file contents
    code = file.read().decode("utf-8")
    linted_code, report = lint_code(code)
    return linted_code, report

# Define the Gradio interface
interface = gr.Interface(
    fn=lint_code,  # Function to be called
    inputs=[
        gr.Textbox(lines=20, placeholder="Paste your Python code here...", label="Python Code"),  # Textbox for code input
        gr.File(label="Upload a Python (.py) file", file_types=[".py"])  # File upload widget
    ],
    outputs=[
        gr.Textbox(label="Linted Code", lines=20),  # Textbox for displaying linted code
        gr.Textbox(label="Linting Report")  # Textbox for displaying linting report
    ],
    title="Python Code Linter",  # Title of the interface
    description="Paste your Python code or upload a .py file to get a Flake8-compliant, linted version."  # Description of the interface
)

# Launch the Gradio interface
interface.launch()
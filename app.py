import gradio as gr
from flake8.api import legacy as flake8
import autopep8

def lint_code(code: str) -> tuple[str, str]:
    """
    Lint the provided Python code using Flake8 and auto-fix it with autopep8.
    Returns the fixed code and the linting report.
    """
    # Run Flake8 for linting, ignoring line-length violations (E501)
    style_guide = flake8.get_style_guide(ignore=["E501"])
    report = style_guide.check_files(None, lines=code.splitlines())
    
    # Auto-fix the code with autopep8
    fixed_code = autopep8.fix_code(code)
    
    # Generate the linting report
    lint_report = "\n".join(msg for msg in report.get_statistics())
    
    return fixed_code, lint_report

def process_file(file) -> tuple[str, str]:
    """
    Process the uploaded file, decode its content, and lint it.
    Returns the fixed code and linting report.
    """
    # Read the file content and decode it to a string
    code = file.read().decode("utf-8")
    
    # Lint the code and get the report
    return lint_code(code)

def handle_input(code: str, file) -> tuple[str, str]:
    """
    Handle both code inputs: either text or file.
    If a file is provided, process the file. Otherwise, process the pasted code.
    """
    if file:
        return process_file(file)
    return lint_code(code)

# Create the Gradio interface
interface = gr.Interface(
    fn=handle_input,
    inputs=[
        gr.Textbox(lines=20, placeholder="Paste your Python code here...", label="Python Code"),
        gr.File(label="Upload a Python (.py) file", file_types=[".py"])
    ],
    outputs=[
        gr.Textbox(label="Linted Code", lines=20),
        gr.Textbox(label="Linting Report")
    ],
    title="Python Code Linter",
    description="Paste your Python code or upload a .py file to get a Flake8-compliant, linted version."
)

# Launch the interface
interface.launch()
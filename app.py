import gradio as gr
from transformers import pipeline
from flake8.api import legacy as flake8
import autopep8

# Initialize the pipeline for text generation
pipe = pipeline("text-generation", model="replit/replit-code-v1_5-3b", trust_remote_code=True)

def generate_code(prompt, max_length=100, num_return_sequences=1):
    try:
        # Use the pipeline to generate code
        results = pipe(prompt, max_length=max_length, num_return_sequences=num_return_sequences)
        # Format the generated results
        return "\n\n".join([res["generated_text"] for res in results])
    except Exception as e:
        return f"An error occurred: {str(e)}"

def lint_code(code: str) -> tuple[str, str]:
    """
    Lint the provided Python code using Flake8 and auto-fix it with autopep8.
    Returns the fixed code and the linting report.
    """
    try:
        # Run Flake8 for linting, ignoring line-length violations (E501)
        style_guide = flake8.get_style_guide(ignore=["E501"])
        
        # Directly check code content
        report = style_guide.check_code(code)
        
        # Auto-fix the code with autopep8
        fixed_code = autopep8.fix_code(code)
        
        # Generate the linting report
        lint_report = "\n".join(msg for msg in report.get_statistics())
        
        return fixed_code, lint_report
    except Exception as e:
        return code, f"An error occurred during linting: {str(e)}"

def process_file(file) -> tuple[str, str]:
    """
    Process the uploaded file, decode its content, and lint it.
    Returns the fixed code and linting report.
    """
    try:
        # Read the file content and decode it to a string
        with file as f:
            code = f.read().decode("utf-8")
        
        # Lint the code and get the report
        return lint_code(code)
    except Exception as e:
        return "", f"An error occurred while processing the file: {str(e)}"

def handle_input(code: str, file) -> tuple[str, str]:
    """
    Handle both code inputs: either text or file.
    If a file is provided, process the file. Otherwise, process the pasted code.
    """
    if file:
        return process_file(file)
    return lint_code(code)

# Gradio interface
with gr.Blocks() as interface:
    gr.Markdown("### PyLint Pro: AI Code Generation Tool")
    
    # Input fields
    prompt_input = gr.Textbox(label="Code Prompt", placeholder="Enter your code snippet or logic...")
    max_length_input = gr.Slider(label="Max Length", minimum=10, maximum=500, value=100)
    num_return_sequences_input = gr.Slider(label="Number of Outputs", minimum=1, maximum=5, value=1)
    
    # Output
    output_box = gr.Textbox(label="Generated Code", placeholder="The generated code will appear here...", lines=10)

    # Button to trigger code generation
    generate_button = gr.Button("Generate Code")
    
    # Define interaction
    generate_button.click(
        generate_code,
        inputs=[prompt_input, max_length_input, num_return_sequences_input],
        outputs=output_box,
    )

    # Existing linting interface
    gr.Markdown("### Python Code Linter")
    code_input = gr.Textbox(lines=20, placeholder="Paste your Python code here...", label="Python Code")
    file_input = gr.File(label="Upload a Python (.py) file", file_types=[".py"])
    linted_code_output = gr.Textbox(label="Linted Code", lines=20)
    lint_report_output = gr.Textbox(label="Linting Report")
    lint_button = gr.Button("Lint Code")
    lint_button.click(
        handle_input,
        inputs=[code_input, file_input],
        outputs=[linted_code_output, lint_report_output],
    )

# Launch the interface
if __name__ == "__main__":
    interface.launch()
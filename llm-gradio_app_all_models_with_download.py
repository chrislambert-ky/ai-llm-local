#This script is a work in progress.
#It is intended to be a Gradio interface for allowing the user to enter a prompt and then running that prompt through vairous models.
#This version also includes the ability to export the responses to a text file.

import gradio as gr
import ollama
import tempfile

#these are the models that are available for selection
#these models are installed using the Ollama library
#ollama run llama3
#ollama run phi3
#ollama run gemma
#ollama run mistral

models = ['mistral', 'gemma', 'phi3', 'llama3']

def generate_responses(user_prompt):
    responses = {}
    
    for model in models:
        response_text = ""
        stream = ollama.chat(model=model, messages=[{'role': 'user', 'content': user_prompt}], stream=True)
        for chunk in stream:
            response_text += chunk['message']['content']
        responses[model] = response_text
    
    return responses['mistral'], responses['gemma'], responses['phi3'], responses['llama3']

def export_to_text_file(user_prompt, mistral_response, gemma_response, phi3_response, llama3_response):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as f:
        f.write("User Prompt:\n")
        f.write(user_prompt + "\n\n")
        f.write("Mistral Response:\n")
        f.write(mistral_response + "\n\n")
        f.write("Gemma Response:\n")
        f.write(gemma_response + "\n\n")
        f.write("Phi3 Response:\n")
        f.write(phi3_response + "\n\n")
        f.write("Llama3 Response:\n")
        f.write(llama3_response + "\n")
        file_path = f.name
    return file_path

def interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Multi-LLM Response Generator")

        user_prompt_input = gr.Textbox(lines=4, placeholder="Enter your prompt here...", label="User Prompt")

        submit_button = gr.Button("Submit Prompt")

        mistral_output = gr.Textbox(lines=10, label="Mistral Response")
        gemma_output = gr.Textbox(lines=10, label="Gemma Response")
        phi3_output = gr.Textbox(lines=10, label="Phi3 Response")
        llama3_output = gr.Textbox(lines=10, label="Llama3 Response")

        submit_button.click(
            fn=generate_responses,
            inputs=user_prompt_input,
            outputs=[mistral_output, gemma_output, phi3_output, llama3_output]
        )

        export_button = gr.Button("Export to Text File")
        
        export_button.click(
            fn=export_to_text_file,
            inputs=[user_prompt_input, mistral_output, gemma_output, phi3_output, llama3_output],
            outputs=gr.File()
        )

    return demo

if __name__ == "__main__":
    demo = interface()
    demo.launch()

#This script is a work in progress.
#It is intended to be a Gradio interface for allowing the user to enter a prompt and then running that prompt through vairous models.

import gradio as gr
import ollama

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

    return demo

if __name__ == "__main__":
    demo = interface()
    demo.launch()

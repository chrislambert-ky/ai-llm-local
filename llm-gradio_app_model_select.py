#This script is a work in progress.
#It is intended to be a Gradio interface for selecting a model from a list of models and interacting with it. 
#The user can select a model from a dropdown list, enter a prompt, and receive a response from the selected model. 

import gradio as gr
import ollama

#these are the models that are available for selection
#these models are installed using the Ollama library
#ollama run llama3
#ollama run phi3
#ollama run gemma
#ollama run mistral

models = ['mistral', 'gemma', 'phi3', 'llama3']

def generate_response(model_name, user_prompt):
    response_text = ""
    stream = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': user_prompt}], stream=True)
    for chunk in stream:
        response_text += chunk['message']['content']
    return response_text

def interface():
    with gr.Blocks() as demo:
        gr.Markdown("# AI Model Interaction Interface")

        with gr.Row():
            model_dropdown = gr.Dropdown(choices=models, label="Select a Model")
        
        user_prompt_input = gr.Textbox(lines=4, placeholder="Enter your prompt here...", label="User Prompt")

        submit_button = gr.Button("Submit Prompt")

        output = gr.Textbox(lines=10, label="AI Model Output")

        submit_button.click(
            fn=generate_response,
            inputs=[model_dropdown, user_prompt_input],
            outputs=output
        )

    return demo

if __name__ == "__main__":
    demo = interface()
    demo.launch()

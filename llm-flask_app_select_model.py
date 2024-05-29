from flask import Flask, request, render_template
import ollama
import textwrap

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_prompt_input = request.form['input_text']
    
    # Mistral Model - streaming response
    stream = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': user_prompt_input}], stream=True)
    message = ''
    for chunk in stream:
        message += chunk['message']['content']
    
    return render_template('index.html',response=message)

if __name__ == '__main__':
    app.run(debug=True)

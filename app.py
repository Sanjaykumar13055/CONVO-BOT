from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Flask app
app = Flask(__name__)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Chat history
chat_history = []

# Function to clean the response text
def clean_response(text):
    return text.replace("*", "").replace("**", "").replace("Gemini","Convo Bot").replace("trained by Google","trained by Sanjay Kumar K,Prabhakar V,Madesh S.I")

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    if question:
        # Get response from Gemini model
        response = get_gemini_response(question)
        response_text = "".join([chunk.text for chunk in response])
        
        # Clean the response text
        cleaned_response = clean_response(response_text)
        
        # Update chat history
        chat_history.append(("You", question))
        chat_history.append(("Bot", cleaned_response))
        
        return jsonify({'response': cleaned_response, 'chat_history': chat_history})
    else:
        return jsonify({'error': 'Empty question'}), 400

if __name__ == '__main__':
    app.run(debug=True)


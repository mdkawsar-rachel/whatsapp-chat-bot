from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import os
import openai

#OpenAI API key
aienv = os.getenv('OPENAI_KEY')
if aienv == None:
    openai.api_key = "Open AI Key"
else:
    openai.api_key = aienv
print(aienv)

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    # Get response from openai
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: ",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    answer = response.choices[0].text
    # Create reply
    resp = MessagingResponse()
    resp.message(answer)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')

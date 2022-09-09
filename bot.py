from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import os
import openai

#OpenAI API key
aienv = os.getenv('OPENAI_KEY')
if aienv == None:
    openai.api_key = "OpenAI Key"
else:
    openai.api_key = aienv
print(aienv)

start_sequence = "\nKotha:"
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
    prompt=f"The following is a conversation with Kotha. She is your virtual friend. She is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nKotha: I am Kotha, your virtual friend created by MD Kawsar Ali. He is a student at Bangabandhu Sheikh Mujibur Rahman Science and Technology University at the department of Pharmacy. How can I help you today?\nHuman: {msg}\nKotha: ",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " Kotha:"]
    )
    answer = response.choices[0].text
    # Create reply
    resp = MessagingResponse()
    resp.message(answer)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')


from flask import Flask, request, jsonify
import nexmo
import os
import requests

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()

client = nexmo.Client(key=os.getenv("NEXMO_API_KEY"), secret=os.getenv("NEXMO_API_SECRET"))

@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    if request.is_json:
        print(request.get_json())
        message = request.get_json()["text"]
        from_number = request.get_json()["msisdn"]
    else:
        data = dict(request.form) or dict(request.args)
        message = data["text"]
        from_number = data["msisdn"]

    prediction = get_prediction(message)
    send_sms(prediction, from_number)

    return ('', 200)

def get_prediction(message):
    url = os.getenv("API_GATEWAY_URL")+ "?message=" + message
    response = requests.request("GET", url)
    return response.json()["prediction"]

def send_sms(message,from_number):
    client.send_message( {
        "from": os.getenv("NEXMO_NUMBER"),
        "to": from_number,
        "text": message
    })
    return client

app.run(port=3000)

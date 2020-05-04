from sklearn.externals import joblib
import pickle
import json

def lambda_handler(event, context):
    #this is the GET parameter passed into the lambda from api gateway
    message  = event["queryStringParameters"]["message"]

    #load the model
    model = joblib.load('model.pkl')

    #load the TFID transformer
    vectorizer = joblib.load('vectorizer.pkl')

    message = vectorizer.transform([message])
    message = message.toarray()
    prediction = model.predict(message)

    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
            "prediction": prediction[0]
        })
    }
    return response

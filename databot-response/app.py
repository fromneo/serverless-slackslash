from chalice import Chalice, Response
import json
import os
import boto3
from dotenv import find_dotenv, load_dotenv
from chalicelib import utils

load_dotenv(find_dotenv())
app = Chalice(app_name='databot-handleresponse')

@app.route('/', methods=['POST'], content_types=['text/plain','application/json'])
def receive():
    headers = app.current_request.headers
    body = json.loads(app.current_request.raw_body)


    # handle the SNS subscription confirmation
    if headers.get('x-amz-sns-message-type') == 'SubscriptionConfirmation':
        client = boto3.client('sns')
        response = client.confirm_subscription(
            TopicArn=os.environ['TOPIC_ARN'],
            Token=body['Token']
        )
    # parse the string
    elif headers.get('x-amz-sns-message-type') == 'Notification':
        # convert strings to json
        try:
            message = json.loads(body['Message'])
        except:
            # assumes that it is already json
            message = body['Message']
        utils.respond(message['text'], message['response_url'])

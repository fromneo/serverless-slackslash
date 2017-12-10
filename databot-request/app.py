from chalice import Chalice, Response
from urlparse import parse_qs
from dotenv import load_dotenv, find_dotenv
import os
import json
import boto3

load_dotenv(find_dotenv())
app = Chalice(app_name='databot-handlerequest')

@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def verify():
    # the raw body is in 'application/x-www-form-urlencoded' so use parse_qs
    request = parse_qs(app.current_request.raw_body)

    if request['token'][0] != os.environ['VERIFICATION_TOKEN']:
        response = Response(
            status_code=403,
            headers={'Content-Type':'application/json'},
            body={'msg':'Forbidden'}
        )
        return response
    # validate the Slack's challenge  (this is required after changing the request URL on slack)
    elif 'challenge' in request:
        response = Response(
            status_code=200,
            headers={'Content-Type':'application/json'},
            body={'challenge':request['challenge']}
        )
        return response
    else:
        # prepare message to send to next lambda service
        message = {
            'response_url': request['response_url'][0],
            'text': request['text'][0]
        }

        # send message
        client = boto3.client('sns')
        publish_topic = client.publish(
            TargetArn=os.environ['TOPIC_ARN'],
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )

        # Return a 200 first since Slack expects a response within 3000ms
        response = Response(
            status_code=200,
            headers={'Content-Type':'application/json'},
            body={
            'response_type':'',
            'text': 'Request received!'}
        )
        return response

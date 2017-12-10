import requests
from commands import *

features = {
    'account': account
}

# send a delayed response to a slack url; this gives time to query the database
def respond(text, response_url):
    payload = parse(text)
    # post the commands back to the channel
    requests.post(
        url = response_url,
        headers = {'content-type': 'application/json'},
        json = {
        'response_type': '',
        'text':'/databot ' + text
        }
    )

    # post the data back to the channel
    r = requests.post(
        url = response_url,
        headers = {'content-type': 'application/json'},
        json = payload
    )

# parse the commands from the user
def parse(text):
    try:
        payload = features[text]()
        return {'text': payload}
    except KeyError:
        return {'text':'That command does not exist.'}

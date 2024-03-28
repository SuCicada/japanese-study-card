import json
import urllib.request
from pprint import pprint


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    # pprint(requestJson)
    res_origin = urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson))
    response = json.load(res_origin)
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# invoke('createDeck', deck='test1')
# result = invoke('deckNames')
# pprint(result)

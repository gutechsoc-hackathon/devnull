import requests, json

URL = 'http://localhost:5000/'
HEADER = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
OK_AUTH = {
        'email' : 'user@test.com',
        'password' : 'pass'
        }
FAIL_AUTH = {
        'email' : 'user',
        'password' : 'something'
        }

OK_PING = {
        'sid' : '',
        'lng' : 50.78,
        'lat' : 50.78,
        'mood' : 0
        }

def url(method):
    return URL + method

response = requests.post(url('auth'), data=json.dumps(OK_AUTH), headers=HEADER)
response = json.loads(response.text)
if not response['error']:
    OK_PING['sid'] = response['data']['sid']
    response = json.loads(requests.post(url('ping'), data=json.dumps(OK_PING), headers=HEADER).text)
    if not response['error'] and 'add' in response['data'] and 'del' in response['data']:
        print("OK AUTH is Ok")

response = requests.post(url('auth'), data=json.dumps({}), headers=HEADER)
response = json.loads(response.text)
if response['error'] and (response['error_message'] == 'Invalid format'):
    print("INVALID FORMAT AUTH is Ok")

response = requests.post(url('auth'), data=json.dumps(FAIL_AUTH), headers=HEADER)
response = json.loads(response.text)
if response['error'] and response['error_message']:
    print("FAIL AUTH is Ok")



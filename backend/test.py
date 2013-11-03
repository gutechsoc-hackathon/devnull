import requests, json

URL = 'http://localhost:5000/'
HEADER = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
OK_DATA = {
        'email' : 'user@test.com',
        'password' : 'pass'
        }
FAIL_DATA = {
        'email' : 'user',
        'password' : 'something'
        }

def url(method):
    return URL + method

print("Testing /auth")
response = requests.post(url('auth'), data=json.dumps(OK_DATA), headers=HEADER)
response = json.loads(response.text)
if not response['error']:
    response = json.loads(requests.post(url('ping'), data=json.dumps({'sid':response['data']['sid']}),headers=HEADER))
    print("\tOK DATA is Ok")

response = requests.post(url('auth'), data=json.dumps({}), headers=HEADER)
response = json.loads(response.text)
if response['error'] and (response['error_message'] == 'Invalid format'):
    print("\tINVALID FORMAT is Ok")

response = requests.post(url('auth'), data=json.dumps(FAIL_DATA), headers=HEADER)
response = json.loads(response.text)
if response['error'] and response['error_message']:
    print("\tFAIL DATA is Ok")



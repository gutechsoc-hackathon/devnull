import requests, json

URL = 'http://localhost:5000/auth'
HEADER = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
OK_DATA = {
        'email' : 'user@test.com',
        'password' : 'pass'
        }
FAIL_DATA = {
        'email' : 'user',
        'password' : 'something'
        }

print("Testing /auth")
response = requests.post(URL, data=json.dumps(OK_DATA), headers=HEADER)
response = json.loads(response.text)
if not response['error'] or response['data']['sid'] == '1234567890':
    print("\tOK DATA is Ok")

response = requests.post(URL, data=json.dumps(FAIL_DATA), headers=HEADER)
response = json.loads(response.text)
if response['error'] and response['error_message']:
    print("\tFAIL DATA is Ok")



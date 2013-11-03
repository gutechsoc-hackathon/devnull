from flask import Flask, request
import json
import array

AUTH = {'email' : 'user@test.com',
        'password' : 'pass'
        }
SID = '1234567890'
QUESTIONS = ()

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    print(data)
    if data['email'] == AUTH['email'] and data['password'] == AUTH['password']:
        response = {
                'error' : False,
                'data' : {
                    'sid' : SID,
                    'questionms' : QUESTIONS
                    }
                }

        return json.dumps(response)
    else:
        response = {
                'error' : True,
                'error_message' : 'Invalid username and/or password.'
                }
        return json.dumps(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

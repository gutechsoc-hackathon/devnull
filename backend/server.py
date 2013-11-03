from flask import Flask, request
import sqlite3
import json

DB_FILE = 'hackathon.db'

AUTH = {'email' : 'user@test.com',
        'password' : 'pass'
        }
SID = '1234567890'
QUESTIONS = ()

app = Flask(__name__)
app.config['DEBUG'] = True

def error(message):
    return json.dumps({'error' : True, 'error_message' : message})

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json(force=True) # fix client to avoid the force

    if 'email' in data.keys() or 'password' in data.keys():
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
            return error('Invalid username and/or password.')
    else:
        return error('Invalid format')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

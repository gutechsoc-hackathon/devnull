from flask import Flask, request, g
import sqlite3
import json


DATABASE = 'hackathon.db'

AUTH = {'email' : 'user@test.com',
        'password' : 'pass'
        }
SID = '1234567890'
QUESTIONS = ()

app = Flask(__name__)
app.config['DEBUG'] = True


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def error(message):
    return json.dumps({'error' : True, 'error_message' : message})


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json(force=True) # fix client to avoid the force

    if 'email' in data.keys() and 'password' in data.keys():
        query = 'SELECT * FROM users WHERE email = ? AND password = ?'
        user = query_db(query, (data['email'], data['password']), one=True)
        if user is None:
            return error('Invalid username and/or password.')
        else:
            response = {
                    'error' : False,
                    'data' : {
                        'sid' : SID,
                        'questionms' : QUESTIONS
                        }
                    }

            return json.dumps(response)
    else:
        return error('Invalid format')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

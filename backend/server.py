from flask import Flask, request, g
import sqlite3
import json
import OpenSSL
import uuid


DATABASE = 'hackathon.db'

AUTH = {'email' : 'user@test.com',
        'password' : 'pass'
        }
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

def generate_session_id(num_bytes = 16):
    # http://stackoverflow.com/questions/817882/unique-session-id-in-python/6092448#6092448
    return str(uuid.UUID(bytes = OpenSSL.rand.bytes(16)))


def login(email, password):
    query = 'SELECT * FROM users WHERE email = ? AND password = ?'
    user = query_db(query, (email, password), one=True)
    if user is None:
        return error('Invalid username and/or password.')
    else:
        sid = generate_session_id()
        query = 'UPDATE users SET session_id = ? WHERE email = ?'
        cursor = get_db().execute(query, (sid, email))

        if cursor.rowcount:
            response = {
                    'error' : False,
                    'data' : {
                        'sid' : sid,
                        'questions' : QUESTIONS
                        }
                    }
            return json.dumps(response)
        else:
            return error('Something')


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json(force=True) # fix client to avoid the force

    if 'email' in data.keys() and 'password' in data.keys():
        return login(data['email'], data['password'])
    else:
        return error('Invalid format')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

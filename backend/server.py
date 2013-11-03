from flask import Flask, request, g
import sqlite3
import json
import OpenSSL
import uuid
import foursquare, json, weather, time, string
from sets import Set
import logging
logging.basicConfig()


DATABASE = 'hackathon.db'

QUESTIONS = ()
FS_CLIENT_ID = 'CD3AGIUUQXJLVJGDPNJH0RSEGJ5M3DEZVFF1VVKM4VFIHULE'
FS_CLIENT_SECRET = 'V0IENWE4MZPFSTKPQ1PWVZF33UUDTEADRHWGJPHBC2ERFIEA'
FS_VERSION = '20131101'


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
    sid = generate_session_id()
    query = 'UPDATE users SET session_id = ?, timestamp = datetime(\'now\', \'localtime\') WHERE email = ?'
    db = get_db()
    cursor = db.execute(query, (sid, email))
    db.commit()

    if cursor.rowcount:
        response = {
                'error' : False,
                'data' : {
                    'sid' : sid,
                    'questions' : QUESTIONS
                    }
                }
        return json.dumps(response)
    
    return error('Couldn\'t login, try again later.')



    


def getVenues(latitude, longitude, client_id, client_secret, version):
    client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, version=version)
    locationString = str(latitude) + ',' + str(longitude)
    venues = client.venues.explore({'ll':locationString, 'radius':500})

    deliverable = [];

    items = venues["groups"][0]["items"]
    for item in items:
        deliverable.append( {"lat":item["venue"]["location"]["lat"], "lng":item["venue"]["location"]["lng"], "name":item["venue"]["name"], "likes":item["venue"]["likes"]["count"], "id":item["venue"]["id"], "cat":item["venue"]["categories"][0]['id']} )

    return deliverable
    
def dealWithTags(validCats, tags, catID, timeVar, temp, weatherType):
    ######## TODO ###########
    ### HANDLE AGE GROUPS ###
    if temp < tags['temp']['lower'] or temp > tags['temp']['upper']:
        validCats.discard(catID);
    if weatherType < tags['weather']['lower'] or weatherType > tags['weather']['upper']:
        validCats.discard(catID);
    timeInt = int(string.replace(timeVar, ":", ""))
    timeCompU = int(tags['time']['upper'])
    timeCompL = int(tags['time']['lower'])
    if timeInt < timeCompL or timeInt > timeCompU:
        validCats.discard(catID)
    return validCats

def get_filtered_venues():
    return filteredVenues


def getData(cid, secret, v):

    venues = getVenues(55.873972, -4.292076, cid, secret, v)

    # For local cache

    catFile = open("algs/cat3.txt")

    cats = json.loads(catFile.readline())

    dateNow = time.strftime("%Y%m%d")
    timeNow = time.strftime("%H:%M")

    weatherTree = weather.get_data()
    # Return dictionary
    weatherData = weather.get_raw_weather(weatherTree, dateNow, timeNow)
    temp = weatherData.attrib['T']
    weatherType = weatherData.attrib['W']

    typeString = weather.weather_type[int(weatherType)]

    #### USER DATA HERE ####

    validCats = Set([])
    validCatsCpy = Set([])
    for venue in venues:
        validCats.add(venue['cat'])
        validCatsCpy.add(venue['cat'])

    # Only care about this part of the file
    cats = cats['response']

    for id in validCatsCpy:
        for mainCategory in cats['categories']:
            # If at least one sub-category exist
            if len(mainCategory['categories']) > 0:
                for subCategory in mainCategory['categories']:
                    if id == subCategory['id'] and 'tags' in subCategory.keys():
                        validCats = dealWithTags(validCats, subCategory['tags'], id, timeNow, temp, weatherType)
                        continue
            elif id == mainCategory['id'] and 'tags' in mainCategory.keys():
                validCats = dealWithTags(validCats, mainCategory['tags'], id, timeNow, temp, weatherType)
                continue

    filteredVenues = [];
    for venue in venues:
        if venue['cat'] in validCats:
            filteredVenues.append(venue)

    return filteredVenues


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json(force=True) # fix client to avoid the force
    keys = data.keys()

    if 'email' in keys and 'password' in keys:
        return login(data['email'], data['password'])
    else:
        return error('Invalid format')

@app.route('/ping', methods=['POST'])
def ping():
    data = request.get_json(force=True)

    if 'sid' in data:
        query = 'SELECT COUNT(*) as count FROM users WHERE session_id = ?'
        user = query_db(query, (data['sid'],), one=True)
        #if not too far from last position, just increment time
        if user and 'id' in user:
            db = get_db()
            query = 'INSERT INTO locations(user_id, lng, lat, mood) VALUES(?, ?, ?, ?)'
            cursor = db.execute(query, (user['id'], data['lng'], data['lat'], data['mood']))
            db.commit()

        #data = getData(FS_CLIENT_ID, FS_CLIENT_SECRET, FS_VERSION)
        #print(len(data))
        #print(data[0])

        response = {
                'error' : False,
                'data' : {
                    'add' : [],
                    'del' : [],
                    'questions' : [],
                    }
                }

        return json.dumps(response)

    return error('Not authenticated') # possibly redirect?


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

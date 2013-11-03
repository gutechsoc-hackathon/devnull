import foursquare
import json
import logging
logging.basicConfig()

### Due to unsolvable errors in the time, this is hardcoded for the latitude and longitude of SAWB, results are JSON text stored in venues.txt

def getVenues(locationJSON):
    location = json.loads(locationJSON)

    latitude = location['latitude']
    longitude = location['longitude']
    
    locationString = str(latitude) + ',' + str(longitude)
    # print client.venues.explore({'near':'Glasgow'})
    venues = client.venues.explore({'ll':locationString, 'radius':200})

    deliverable = [];

    items = venues["groups"][0]["items"]
    for item in items:
        deliverable.append( {"lat":item["venue"]["location"]["lat"], "lng":item["venue"]["location"]["lng"], "name":item["venue"]["name"], "likes":item["venue"]["likes"]["count"], "id":item["venue"]["id"]} )

    return json.dumps(deliverable)


client = foursquare.Foursquare(client_id='CD3AGIUUQXJLVJGDPNJH0RSEGJ5M3DEZVFF1VVKM4VFIHULE', client_secret='V0IENWE4MZPFSTKPQ1PWVZF33UUDTEADRHWGJPHBC2ERFIEA', version='20131101')

obj_json = u'{"latitude": 55.873972, "longitude": -4.292076}'

venues = getVenues(obj_json)

f = open("venues.txt", "w")
f.write(venues)
f.close()

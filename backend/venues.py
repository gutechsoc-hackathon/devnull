import foursquare
import json
import logging
logging.basicConfig()

def getVenues(latitude, longitude):
    locationString = str(latitude) + ',' + str(longitude)
    venues = client.venues.explore({'ll':locationString, 'radius':500})

    deliverable = [];

    items = venues["groups"][0]["items"]
    for item in items:
        deliverable.append( {"lat":item["venue"]["location"]["lat"], "lng":item["venue"]["location"]["lng"], "name":item["venue"]["name"], "likes":item["venue"]["likes"]["count"], "id":item["venue"]["id"], "cat":item["venue"]["categories"][0]['id']} )

    return json.dumps(deliverable)


client = foursquare.Foursquare(client_id='CD3AGIUUQXJLVJGDPNJH0RSEGJ5M3DEZVFF1VVKM4VFIHULE', client_secret='V0IENWE4MZPFSTKPQ1PWVZF33UUDTEADRHWGJPHBC2ERFIEA', version='20131101')

obj_json = u'{"latitude": 55.873972, "longitude": -4.292076}'

venues = getVenues(55.873972, -4.292076)

f = open("venues.txt", "w")
f.write(venues)
f.close()

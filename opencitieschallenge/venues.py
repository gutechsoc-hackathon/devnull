import foursquare
import json
import logging
logging.basicConfig()

def getVenues(locationJSON):
    location = json.loads(locationJSON)

    latitude = location['latitude']
    longitude = location['longitude']
    print latitude
    print longitude
    locationString = str(latitude) + ',' + str(longitude)
    # print client.venues.explore({'near':'Glasgow'})
    return client.venues.explore({'ll':locationString, 'radius':100})




client = foursquare.Foursquare(client_id='CD3AGIUUQXJLVJGDPNJH0RSEGJ5M3DEZVFF1VVKM4VFIHULE', client_secret='V0IENWE4MZPFSTKPQ1PWVZF33UUDTEADRHWGJPHBC2ERFIEA', version='20131101')

# print client.venues.explore({'ll':'55.8580,-4.2590'})




obj_json = u'{"latitude": 55.8580, "longitude": -4.2590}'

venues = getVenues(obj_json)
print venues

#location = json.loads(obj_json)

#location2 = getVenues(obj_json)

#print(repr(location))

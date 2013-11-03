import foursquare, json, weather, time, string, logging
from sets import Set
logging.basicConfig()

def getVenues(latitude, longitude):
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



client = foursquare.Foursquare(client_id='CD3AGIUUQXJLVJGDPNJH0RSEGJ5M3DEZVFF1VVKM4VFIHULE', client_secret='V0IENWE4MZPFSTKPQ1PWVZF33UUDTEADRHWGJPHBC2ERFIEA', version='20131101')

obj_json = u'{"latitude": 55.873972, "longitude": -4.292076}'

venues = getVenues(55.873972, -4.292076)

# For local cache

f = open("venues.txt", "w")
f.write(json.dumps(venues))
f.close()

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

#print filteredVenues
#print "Before: " + str(len(venues)) + " After: " + str(len(filteredVenues))
                        
                    
                


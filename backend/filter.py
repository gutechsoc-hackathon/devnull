import json, weather, time, string
from venues.py import getVenues
from sets import Set

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

venuesFile = open("venues.txt")
catFile = open("algs/cat3.txt")

venues = json.loads(venuesFile.readline())
cats = json.loads(catFile.readline())

dateNow = time.strftime("%Y%m%d")
timeNow = time.strftime("%H:%M")

weatherTree = weather.get_data()
# Return dictionary
weatherData = weather.get_raw_weather(weatherTree, dateNow, timeNow)
temp = weatherData.attrib['T']
weatherType = weatherData.attrib['W']
#print weatherType

typeString = weather.weather_type[int(weatherType)]
#print typeString

#### USER DATA HERE ####

validCats = Set([])
validCatsCpy = Set([])
for venue in venues:
    validCats.add(venue['cat'])
    validCatsCpy.add(venue['cat'])

#print cats
#print
#print
#print
#print venues
#print
#print
#print

# Only care about this part of the file
cats = cats['response']
#print cats
#print
#print
#print

for id in validCatsCpy:
    for mainCategory in cats['categories']:
        #print mainCategory
        #print
        #print
        #print
        # If at least one sub-category exist
        if len(mainCategory['categories']) > 0:
            for subCategory in mainCategory['categories']:
                #print subCategory
                #print
                #print
                #print
                if id == subCategory['id'] and 'tags' in subCategory.keys():
                    validCats = dealWithTags(validCats, subCategory['tags'], id, timeNow, temp, weatherType)
                    continue
        elif id == mainCategory['id'] and 'tags' in mainCategory.keys():
            validCats = dealWithTags(validCats, mainCategory['tags'], id, timeNow, temp, weatherType)
            continue


#They're different!
#print validCatsCpy
#print validCats

#print venues
#print
#print
#print

filteredVenues = [];
for venue in venues:
    if venue['cat'] in validCats:
        filteredVenues.append(venue)
    
#print get_filtered_venues()

#print filteredVenues
#print "Before: " + str(len(venues)) + " After: " + str(len(filteredVenues))
                        
                    
                


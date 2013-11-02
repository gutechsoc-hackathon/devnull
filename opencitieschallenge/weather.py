import requests, time
import xml.etree.ElementTree as ET

weather_type = [
"Not available",
"Clear night",
"Sunny day",
"Partly cloudy (night)",
"Partly cloudy (day)",
"Not used",
"Mist",
"Fog",
"Cloudy",
"Overcast",
"Light rain shower (night)",
"Light rain shower (day)",
"Drizzle",
"Light rain",
"Heavy rain shower (night)",
"Heavy rain shower (day)",
"Heavy rain",
"Sleet shower (night)",
"Sleet shower (day)",
"Sleet",
"Hail shower (night)",
"Hail shower (day)",
"Hail",
"Light snow shower (night)",
"Light snow shower (day)",
"Light snow",
"Heavy snow shower (night)",
"Heavy snow shower (day)",
"Heavy snow",
"Thunder shower (night)",
"Thunder shower (day)", 
"Thunder"]

def get_data():
	r = requests.get('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/310009?res=3hourly&key=d73af5c0-e626-4591-ab9b-ef36f4d8956c')

	return ET.fromstring(r.text)

def get_params(root):
	wtherdict = {}
	for p in root[0]:
		wtherdict[p.text] = p.attrib
	return wtherdict

def get_raw_weather(root, in_date, in_time):
	cur_date = time.strftime("%Y%m%d")
	
	if ((int)(in_date) > (int)(cur_date) + 4 or (int)(in_date) < (int)(cur_date)):
		print("Date Specificed outside Predition Bounds!") 
		return

	for p in root[1][0]:
		this_date = p.attrib['value'][0:-1].replace('-', '')
		if (this_date == in_date):
			data = p
			break

	time_hours = (int)(in_time[0:2]) * 60
	for p in data:
		if (time_hours <= (int)(p.text)):
			return p
			break

def get_weather(root, in_date, in_time):
	wd = get_params(root)
	
	rw = get_raw_weather(root, in_date, in_time)

	weth = []

	for n in wd:
		if (n == "Weather Type"):
			weth.append(n + ": " + weather_type[(int)(rw.attrib[wd[n]['name']])])

		weth.append((n + ": " + rw.attrib[wd[n]['name']] + " " + wd[n]['units']))
	
	return weth

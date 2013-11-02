import requests
import xml.etree.ElementTree as ET

def get_data():
		r = requests.get('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/310009?res=3hourly&key=d73af5c0-e626-4591-ab9b-ef36f4d8956c')

		r = requests.get(url)

	return ET.fromstring(r.text)

def get_params(root):
	wtherdict = {}
	for p in root[0]:
		wtherdict[p.text] = p.attrib
	return wd

def get_raw_weather(root, date, time)
	wd = get_params(root)

	

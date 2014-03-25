from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen

OUTDIV = "front-lists"
MAPPING = {"front-lists": ["card-v2", "name","meta"] }

def getData(url_root="http://www.listnerd.com", path="", outdiv=OUTDIV):
	url = url_root + '/' + path
	soup = bs(urlopen(url))

	found = soup.findAll('div', {"id": outdiv})

	toreturn = {}

	if not found:
		return None

	else:
		innerDiv = MAPPING[outdiv][0]
		attributes = MAPPING[outdiv][1:]

		allitems = soup.findAll(attrs={"class":innerDiv})

		index = 0

		for item in allitems:	
			toreturn[index] = {}

			for attr in attributes:
				toreturn[index][attr] = item.findAll(attrs={"class":attr})[0].text

			index += 1

	
		return toreturn
from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen

OUTDIV = "front-lists"
MAPPING = {"front-lists": ["card-v2", "name","meta"] }

def getData(url_root="http://www.listnerd.com", path="", name="front-lists"):
	if name == "front-lists":
		outdiv = "front-lists"
		mapping = MAPPING
		path = ""
	elif name == "list":
		outdiv = "thelist-list"
		mapping = {"thelist-list" : ["item", "position", "title", "vote"]}
		path = "list/top-10-video-game-developers"
	else:
		outdiv = "thelist-list"
		mapping = MAPPING
		path = ""

	url = url_root + '/' + path
	soup = bs(urlopen(url))

	found = soup.findAll(attrs = {"id":outdiv})
	if not found:
		found = soup.findAll(attrs = {"class":outdiv})

	toreturn = {}

	if not found:
		return None

	else:
		innerDiv = mapping[outdiv][0]
		attributes = mapping[outdiv][1:]

		allitems = soup.findAll(attrs={"class":innerDiv})

		index = 0

		for item in allitems:	
			toreturn[index] = {}

			found = []
			for attr in attributes:
				found = item.findAll(attrs = {"class":attr})
				if found:
					toreturn[index][attr] = item.findAll(attrs={"class":attr})[0].text.strip()
			if found:
				index += 1

		if not found:
			del(toreturn[index])

		print toreturn
		return toreturn
from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen

OUTDIV = "front-lists"
MAPPING = {"front-lists": ["card-v2", "name","meta"] }

def getData(url_root="http://www.listnerd.com", path="", name="frontpage"):
	if url_root == "http://www.listnerd.com":
		if name == "frontpage":
			outdiv = "front-lists"
			mapping = MAPPING
			path = ""
		elif name == "list":
			outdiv = "thelist-list"
			mapping = {"thelist-list" : ["item", "position", "title", "vote"]}
			path = "list/" + path
			if path == "":
				path = "list/top-10-video-game-developers"
		elif name == "search":
			outdiv ="searchResult"
			mapping = {"searchResult" : ["card", "name", "description", "meta"]}
			path = "search?query=" + path
			if path == "":
				path = "search?query=netflix"
		else:
			outdiv = "front-lists"
			mapping = MAPPING
			path = ""
	elif url_root == "http://www.picturegr.am":
		if name == "frontpage":
			outdiv = "container"
			mapping = { "container" : ["col-xs-12","thumbnail"], "arefs" : [False, True] }
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

		if "arefs" in mapping:
			attr_aref = mapping["arefs"][1:]

		allitems = soup.findAll(attrs={"class":innerDiv})

		index = 0

		for item in allitems:	
			toreturn[index] = {}

			found = []
			for attr in attributes:
				found = item.findAll(attrs = {"class":attr})
				if found:
					toreturn[index][attr] = item.findAll(attrs={"class":attr})[0].text.strip()
					if attr_aref != None and attr_aref[attributes.index((attr))]:
						if 'href' in item.findAll(attrs={"class":attr})[0]:
							toreturn[index][attr+"_href"] = item.findAll(attrs={"class":attr})[0]['href']
			if found:
				index += 1

		if not found:
			del(toreturn[index])

		print toreturn
		return toreturn
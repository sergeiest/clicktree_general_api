from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen

OUTDIV = "front-lists"
MAPPING = {"front-lists": {"innerdiv" : "card-v2", "name" : "text" , "meta" : "text"} }

def getData(url_root="http://www.listnerd.com", path="", name="frontpage"):
	if url_root == "http://www.listnerd.com":
		if name == "frontpage":
			outdiv = "front-lists"
			mapping = MAPPING
			path = ""
		elif name == "list":
			outdiv = "thelist-list"
			mapping = {"thelist-list" : {"innerdiv" : "item", "position" : "text", "title" : "text", "vote": "text"} }
			if not path.startswith('list/'):
				path = "list/" + path
			if path == "":
				path = "list/top-10-video-game-developers"
		elif name == "search":
			outdiv ="searchResult"
			mapping = {"searchResult" : { "innerdiv" : "card", "name" : "text", "description" : "text", "meta" : "text"} }
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
			mapping = { "container" : { "innerdiv" : "col-xs-12", "thumbnail": "href" } }
			path = ""
		if name == "picture":
			outdiv = "container"
			mapping = { "container" : { "innerdiv" : "row", "fillWidth" : "src", "likes" : "text", "comments": "text", "authorlink" : "text"}}
			if not path.startswith('picture/'):
				path = name + '/' + path
		if name == "search":
			outdiv = "container"
			mapping = { "container" : { "innerdiv" : "col-xs-12", "thumbnail": "href" } }
			path = "tag/" + path

	url = url_root + '/' + path
	print "url: " + url 
	soup = bs(urlopen(url))

	found = soup.findAll(attrs = {"id":outdiv})
	if not found:
		found = soup.findAll(attrs = {"class":outdiv})

	toreturn = {}

	if not found:
		return None

	else:
		innerDiv = mapping[outdiv]["innerdiv"]
		attributes = [key for key in mapping[outdiv].keys() if key != "innerdiv"]
		innerDivDict = mapping[outdiv]
		allitems = []
		foundOne = False
		index = 0

		for each in found:
			tempitems = findClassorId(each, innerDiv)
			if tempitems:
				allitems.extend(tempitems)


		for item in allitems:	
			print item
			toreturn[index] = {}
			foundOne = False

			for attr in attributes:
				elemdata = getElementData(item, attr, innerDivDict[attr])

				if elemdata != None:
					foundOne = True
					toreturn[index][elemdata[0]] = elemdata[1]

			if foundOne:
				index += 1

			if not foundOne:
				del(toreturn[index])

		print toreturn
		return toreturn


def getElementData(wholeitem, tag_name, type_tag):
	print "wholeitem " + str(wholeitem)
	print "tag_name " + tag_name
	print "type_tag " + type_tag
	found = []
	datatoreturn = None

	found = findClassorId(wholeitem, tag_name)

	print "found in element data"

	if found: 
		if type_tag != "text":
			print "not text"
			if found[0].has_attr(type_tag):
				data = found[0][type_tag]
				datatoreturn = (tag_name + '_' + type_tag, data)

		else:
			print found[0]
			data = found[0].text.strip()
			datatoreturn = (tag_name, data)
 
	return datatoreturn


def findClassorId(item, name):
	found = []
	found = item.findAll(attrs = { "class":name })
	if not found:
		found = item.findAll(attrs = { "id":name })

	return found
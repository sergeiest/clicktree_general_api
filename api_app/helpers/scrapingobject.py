from scraperhelper import getData

class ScrapingObject(object):
	def __init__(self, url_root="http://www.listnerd.com", path="", outdiv='front-lists'):
		self.data = []

		self.populateData(url_root, path, outdiv)

	def populateData(self, url_root, path, outdiv):
		forPopulate = getData(url_root, path, outdiv)
		if forPopulate:
			index = 0
			for key, value in forPopulate.items():
				self.data.append({"index":key})
				
				for key2, value2 in value.items():
					self.data[index][key2] = value2

				index += 1



class dict2obj(object):

	def __init__(self, d):
		self.__dict__['d'] = d
 
	def __getattr__(self, key):
		value = self.__dict__['d'][key]
		if type(value) == type({}):
			return dict2obj(value)
 
		return value
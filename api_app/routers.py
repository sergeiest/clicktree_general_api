

class ApiRouter(object):

	def db_for_read(self, model, **hints):
		"""
		Attempts to read auth models go to auth_db.
		"""
		if model._meta.app_label == 'dev_users':
			return 'dev_users_db'
		return None

	def db_for_write(self, model, **hints):
		"""
		Attempts to write auth models go to auth_db.
		"""
		if model._meta.app_label == 'dev_users':
			return 'dev_users_db'
		return None

	def allow_relation(self, obj1, obj2, **hints):
		"""
		Allow relations if a model in the auth app is involved.
		"""
		if obj1._meta.app_label == 'dev_users' or \
			obj2._meta.app_label == 'dev_users':
			return True
		return None
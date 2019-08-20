import json
import os.path

class Storage:

	storage_file = None

	def __init__(self, storage_file):
		self.storage_file = storage_file

	def save(self, secrets):
		with open(self.storage_file, "w") as handle:
			json.dump(secrets, handle)
	
	def read(self):
		if not os.path.exists(self.storage_file):
			return { }
		with open(self.storage_file, "r") as handle:
			return json.load(handle)
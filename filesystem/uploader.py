import os

import requests


class FileManagerConfig:
	def __init__(self, username, password, auth_title, driver):
		self.username = username
		self.password = password
		self.auth_title = auth_title
		self.driver = driver


class FileManager:
	def __init__(self, config=None):
		self.err = None
		self.dst_dir = ""
		self.src_dir = ""
		self.file_bytes = b""
		self.file_size = 0
		self.config = config

	@staticmethod
	def new(config):
		return FileManager(config)

	@staticmethod
	def new_by_local_file(src_dir, dst_dir, config):
		if not os.path.exists(src_dir):
			raise FileNotFoundError("Target file does not exist")

		with open(src_dir, 'rb') as f:
			file_bytes = f.read()

		return FileManager(config).give_src_dir(src_dir).give_dst_dir(dst_dir).give_file_bytes(file_bytes)

	@staticmethod
	def new_by_bytes(src_file_bytes, dst_dir, config):
		return FileManager(config).give_dst_dir(dst_dir).give_file_bytes(src_file_bytes)

	def give_src_dir(self, src_dir):
		if not os.path.exists(src_dir):
			raise FileNotFoundError("Target file does not exist")

		with open(src_dir, 'rb') as f:
			self.file_bytes = f.read()

		self.src_dir = src_dir
		self.file_size = len(self.file_bytes)
		return self

	def give_dst_dir(self, dst_dir):
		self.dst_dir = dst_dir
		return self

	def give_file_bytes(self, file_bytes):
		self.file_bytes = file_bytes
		self.file_size = len(file_bytes)
		return self

	def upload(self):
		if self.config.driver == "LOCAL":
			return self.upload_to_local()
		elif self.config.driver == "NEXUS":
			return self.upload_to_nexus()
		elif self.config.driver == "OSS":
			return self.upload_to_oss()
		else:
			raise ValueError(f"Unsupported driver type: {self.config.driver}")

	def delete(self):
		if self.config.driver == "LOCAL":
			return self.delete_from_local()
		elif self.config.driver == "NEXUS":
			return self.delete_from_nexus()
		elif self.config.driver == "OSS":
			return self.delete_from_oss()
		else:
			raise ValueError(f"Unsupported driver type: {self.config.driver}")

	def upload_to_local(self):
		with open(self.dst_dir, 'wb') as f:
			written = f.write(self.file_bytes)
		return written

	def upload_to_nexus(self):
		headers = {
			"Content-Length": str(self.file_size),
			"Authorization": f"{self.config.auth_title} {self.config.username}:{self.config.password}"
		}
		response = requests.put(self.dst_dir, headers=headers, data=self.file_bytes)
		response.raise_for_status()
		return len(self.file_bytes)

	def upload_to_oss(self):
		raise NotImplementedError("OSS upload is not supported yet")

	def delete_from_local(self):
		if os.path.exists(self.dst_dir):
			os.remove(self.dst_dir)
		else:
			raise FileNotFoundError("Target file does not exist")

	def delete_from_nexus(self):
		headers = {"Authorization": f"{self.config.auth_title} {self.config.username}:{self.config.password}"}
		response = requests.delete(self.dst_dir, headers=headers)
		response.raise_for_status()

	def delete_from_oss(self):
		raise NotImplementedError("OSS delete is not supported yet")

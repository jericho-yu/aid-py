import hashlib


def md5(original: bytes) -> str:
	hash_object = hashlib.md5()
	hash_object.update(original)
	return hash_object.hexdigest()


if __name__ == "__main__":
	# Example usage
	original_data = b"example data"
	encoded_data = md5(original_data)
	print(encoded_data)

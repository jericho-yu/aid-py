import hashlib


def sha256(original: bytes) -> str:
	hash_object = hashlib.sha256()
	hash_object.update(original)
	return hash_object.hexdigest()


if __name__ == "__main__":
	# Example usage
	original_data = b"example data"
	encoded_data = sha256(original_data)
	print(encoded_data)

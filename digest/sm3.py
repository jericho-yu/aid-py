from gmssl import sm3, func

def sm3_hash(original: bytes) -> str:
    hash_value = sm3.sm3_hash(func.bytes_to_list(original))
    return hash_value

if __name__ == "__main__":
	# Example usage
	original_data = b"example data"
	encoded_data = sm3_hash(original_data)
	print(encoded_data)
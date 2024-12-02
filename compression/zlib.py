import zlib

class Zlib:
	def compress(self, original_data: bytes) -> bytes:
		try:
			return zlib.compress(original_data)
		except Exception as e:
			raise RuntimeError(f"Compression error: {e}")

	def decompress(self, data: bytes) -> bytes:
		try:
			return zlib.decompress(data)
		except Exception as e:
			raise RuntimeError(f"Decompression error: {e}")

if __name__ == '__main__':
	# Example usage
	zlib_instance = Zlib()
	compressed_data = zlib_instance.compress(b"example data")
	decompressed_data = zlib_instance.decompress(compressed_data)
	print(decompressed_data)
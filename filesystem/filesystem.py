import shutil
from pathlib import Path


class FileSystem:
	def __init__(self, dir_path: str):
		self.dir = Path(dir_path).resolve()
		self.is_exist = self.dir.exists()
		self.is_dir = self.dir.is_dir()
		self.is_file = self.dir.is_file()

	@staticmethod
	def new_by_abs(dir: str) -> "FileSystem":
		return FileSystem(dir=dir).init()

	@staticmethod
	def new_by_relative(dir: str) -> "FileSystem":
		return FileSystem(Path(".").resolve() / dir)

	def copy(self) -> "FileSystem":
		return FileSystem(self.dir)

	def set_dir_by_relative(self, dir_path: str) -> "FileSystem":
		root_path = Path(".").resolve()
		self.dir = (root_path / dir_path).resolve()
		self._init()
		return self

	def set_dir_by_abs(self, dir_path: str) -> "FileSystem":
		self.dir = Path(dir_path).resolve()
		self._init()
		return self

	def join(self, dir_path: str) -> "FileSystem":
		self.dir = self.dir / dir_path
		self._init()
		return self

	def joins(self, *dir_paths: str) -> "FileSystem":
		for dir_path in dir_paths:
			self.join(dir_path)
		self._init()
		return self

	@staticmethod
	def get_root_path() -> str:
		return str(Path(".").resolve())

	@staticmethod
	def get_current_path() -> str:
		return str(Path(__file__).resolve().parent)

	def _init(self) -> "FileSystem":
		self.is_exist = self.dir.exists()
		self.is_dir = self.dir.is_dir()
		self.is_file = self.dir.is_file()
		return self

	def exist(self) -> bool:
		return self.is_exist

	def mkdir(self) -> None:
		if not self.is_exist:
			self.dir.mkdir(parents=True, exist_ok=True)
			self._init()

	def get_dir(self) -> str:
		return str(self.dir)

	def check_path_type(self) -> None:
		self.is_dir = self.dir.is_dir()
		self.is_file = self.dir.is_file()

	def delete(self) -> None:
		if self.is_exist:
			if self.is_dir:
				shutil.rmtree(self.dir)
			elif self.is_file:
				self.dir.unlink()
			self._init()

	def read(self) -> bytes:
		if self.is_file:
			return self.dir.read_bytes()
		raise FileNotFoundError(f"{self.dir} is not a file")

	def rename_file(
		self, new_filename: str, delete_repetition: bool = False
	) -> "FileSystem":
		new_path = self.dir.parent / new_filename
		if delete_repetition and new_path.exists():
			new_path.unlink()
		self.dir.rename(new_path)
		return FileSystem(new_path)

	def copy_file(self, dst_dir: str, dst_filename: str = "", abs: bool = False) -> str:
		dst_path = Path(dst_dir).resolve() if abs else (Path(".").resolve() / dst_dir)
		if not dst_path.exists():
			dst_path.mkdir(parents=True, exist_ok=True)
		dst_file = dst_path / (dst_filename or self.dir.name)
		shutil.copy2(self.dir, dst_file)
		return str(dst_file)

	def copy_files(self, src_files: list, dst_dir: str, abs: bool = False) -> None:
		dst_path = Path(dst_dir).resolve() if abs else (Path(".").resolve() / dst_dir)
		if not dst_path.exists():
			dst_path.mkdir(parents=True, exist_ok=True)
		for src_file in src_files:
			src_file.copy_file(dst_path)

	def copy_dir(self, dst_dir: str, abs: bool = False) -> None:
		if not self.is_dir:
			raise NotADirectoryError(f"{self.dir} is not a directory")
		dst_path = Path(dst_dir).resolve() if abs else (Path(".").resolve() / dst_dir)
		shutil.copytree(self.dir, dst_path, dirs_exist_ok=True)

	def write_bytes(self, content: bytes) -> int:
		with self.dir.open("wb") as f:
			return f.write(content)

	def write_string(self, content: str) -> int:
		return self.write_bytes(content.encode())

	def write_io_reader(self, content) -> int:
		with self.dir.open("wb") as f:
			return f.write(content.read())

	def write_bytes_append(self, content: bytes) -> int:
		with self.dir.open("ab") as f:
			return f.write(content)

	def write_string_append(self, content: str) -> int:
		return self.write_bytes_append(content.encode())

	def write_io_reader_append(self, content) -> int:
		with self.dir.open("ab") as f:
			return f.write(content.read())


if __name__ == "__main__":
	print(new_by_relative("").joins("abc.txt").write_string("abc"))

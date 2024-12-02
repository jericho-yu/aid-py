import threading
from typing import List, Callable, Any, Dict

def new(array: List[Any]) -> 'AnyArray':
	return AnyArray(array)


def make(length: int) -> 'AnyArray':
	return AnyArray([None] * length)


class AnyArray:
	def __init__(self, array: List[Any]) -> None:
		self.array = array
		self.lock = threading.Lock()

	def is_empty(self) -> bool:
		"""
		判断是否为空
		:return: bool
		"""
		with self.lock:
			return len(self.array) == 0

	def is_not_empty(self) -> bool:
		"""
		判断是否不为空
		:return: bool
		"""
		with self.lock:
			return len(self.array) > 0

	def has(self, index: int) -> bool:
		"""
		判断是否有指定索引
		:param index: int
		:return: bool
		"""
		with self.lock:
			return 0 <= index < len(self.array)

	def set(self, index: int, value: Any) -> 'AnyArray':
		"""
		设置指定索引的值
		:param index: int
		:param value: Any
		:return: AnyArray
		"""
		with self.lock:
			if self.has(index):
				self.array[index] = value
		return self

	def get(self, index: int) -> Any:
		"""
		获取指定索引的值
		:param index: int
		:return: Any
		"""
		with self.lock:
			return self.array[index] if self.has(index) else None

	def append(self, value: Any) -> 'AnyArray':
		"""
		添加元素
		:param value: Any
		:return: AnyArray
		"""
		with self.lock:
			self.array.append(value)
		return self

	def first(self) -> Any:
		"""
		获取第一个元素
		:return: Any
		"""
		with self.lock:
			return self.array[0] if self.is_not_empty() else None

	def last(self) -> Any:
		"""
		获取最后一个元素
		:return: Any
		"""
		with self.lock:
			return self.array[-1] if self.is_not_empty() else None

	def to_array(self) -> List[Any]:
		"""
		获取数组
		:return: List[Any]
		"""
		with self.lock:
			return self.array

	def get_index_by_value(self, value: Any) -> int:
		"""
		获取指定值的索引
		:param value: Any
		:return: int
		"""
		with self.lock:
			return self.array.index(value) if value in self.array else -1

	def copy(self) -> 'AnyArray':
		"""
		复制自己
		:return: AnyArray
		"""
		with self.lock:
			return AnyArray(self.array.copy())

	def shuffle(self) -> 'AnyArray':
		"""
		打乱数组
		:return: AnyArray
		"""
		import random
		with self.lock:
			random.shuffle(self.array)
		return self

	def len(self) -> int:
		"""
		获取数组长度
		:return: int
		"""
		with self.lock:
			return len(self.array)

	def filter(self, fn: Callable[[Any], bool]) -> 'AnyArray':
		"""
		过滤数组
		:param fn: Callable[[Any], bool]
		:return: AnyArray
		"""
		with self.lock:
			self.array = [arr for arr in self.array if fn(arr)]

		return self

	def remove_empty(self) -> 'AnyArray':
		"""
		移除空元素
		:return: AnyArray
		"""
		with self.lock:
			self.array = [arr for arr in self.array if arr]

		return self

	def join(self, sep: str) -> str:
		"""
		连接数组
		:param sep: str
		:return: AnyArray
		"""
		with self.lock:
			return sep.join(self.array)

	def join_without_empty(self, sep: str) -> str:
		"""
		连接数组并移除空元素
		:param sep: str
		:return: str
		"""
		with self.lock:
			return sep.join(self.copy().remove_empty().array)

	def in_array(self, target: Any) -> bool:
		"""
		判断是否在数组中
		:param target:
		:return:
		"""
		with self.lock:
			return target in self.array

	def not_in(self, target: Any) -> bool:
		"""
		判断是否不在数组中
		:param target:
		:return:
		"""
		with self.lock:
			return not self.in_array(target)

	def all(self) -> bool:
		"""
		判断是否所有元素
		:return: bool
		"""
		with self.lock:
			return all(self.array)

	def any(self) -> bool:
		"""
		判断是否有元素
		:return: bool
		"""
		with self.lock:
			return any(self.array)

	def chunk(self, size: int) -> List[List[Any]]:
		"""
		分割数组
		:param size: int
		:return: List[List[Any]]
		"""
		with self.lock:
			return [self.array[i:i + size] for i in range(0, len(self.array), size)]

	def pluck(self, key: str) -> 'AnyArray':
		"""
		提取数组中的属性
		:param key: str
		:return: AnyArray
		"""
		with self.lock:
			self.array = [getattr(arr, key) for arr in self.array]

			return self

	def unique(self) -> 'AnyArray':
		"""
		去重
		:return: AnyArray
		"""
		with self.lock:
			seen = set()
			result = []
			for arr in self.array:
				if arr not in seen:
					seen.add(arr)
					result.append(arr)
			return self

	def remove_by_indexes(self, indexes: int) -> 'AnyArray':
		"""
		移除指定索引的元素
		:param indexes: int
		:return: AnyArray
		"""
		with self.lock:
			self.array = [arr for i, arr in enumerate(self.array) if i not in indexes]

		return self

	def remove_by_value(self, values: List[Any]) -> 'AnyArray':
		"""
		移除指定值的元素
		:param values: List[Any]
		:return: AnyArray
		"""
		with self.lock:
			self.array = [arr for arr in self.array if arr not in values]

		return self

	def remove_by_values(self, values: List[Any]) -> 'AnyArray':
		"""
		移除指定值的元素
		:param values: List[Any]
		:return: AnyArray
		"""
		with self.lock:
			self.array = [arr for arr in self.array if arr not in values]

		return self

	def map(self, fn: Callable[[Any], Any]) -> 'AnyArray':
		"""
		判断每一个元素是否符合条件
		:param fn:
		:return:
		"""
		with self.lock:
			self.array = [arr for arr in self.array if fn(arr)]
			return self

	def max(self) -> Any:
		"""
		获取最大值
		:return: Any
		"""
		with self.lock:
			return max(self.array)

	def min(self) -> Any:
		"""
		获取最小值
		:return: Any
		"""
		with self.lock:
			return min(self.array)

	def sum(self) -> Any:
		"""
		求和
		:return: Any
		"""
		with self.lock:
			return sum(self.array)

	def avg(self) -> float:
		"""
		获取平均值
		:return: float
		"""
		with self.lock:
			return sum(self.array) / len(self.array)

	def group_by(self, key: str) -> Dict[Any, List[Any]]:
		"""
		分组
		:param key: str
		:return: Dict[Any, List[Any]]
		"""
		with self.lock:
			result = {}
			for arr in self.array:
				k = getattr(arr, key)
				if k not in result:
					result[k] = []
				result[k].append(arr)
			return result

	def clean(self) -> 'AnyArray':
		"""
		清空数组
		:return: AnyArray
		"""
		with self.lock:
			self.array.clear()
		return self
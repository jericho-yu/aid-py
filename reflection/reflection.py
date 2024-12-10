import inspect
import time
import types

class Reflection:
    def __init__(self, obj):
        self.original = obj
        self.ref_type = type(obj)
        self.is_ptr = isinstance(obj, (list, dict, set, tuple))
        self.is_zero = obj is None or (self.is_ptr and len(obj) == 0)
        self.is_time = isinstance(obj, time.struct_time)

    def get_value(self):
        return self.original

    def get_type(self):
        return self.ref_type

    def get_reflection_type(self):
        if self.is_time:
            return "DATETIME"
        if self.is_zero:
            return "NIL"
        if isinstance(self.original, int):
            return "INT"
        if isinstance(self.original, float):
            return "FLOAT"
        if isinstance(self.original, str):
            return "STRING"
        if isinstance(self.original, bool):
            return "BOOL"
        if isinstance(self.original, list):
            return "ARRAY"
        if isinstance(self.original, dict):
            return "MAP"
        if isinstance(self.original, types.FunctionType):
            return "FUNCTION"
        return "UNKNOWN"

    def is_same(self, value):
        return self.ref_type == type(value)

    def is_same_deep_equal(self, value):
        return self.original == value

    def call_method_by_name(self, method_name, *args, **kwargs):
        method = getattr(self.original, method_name, None)
        if callable(method):
            return method(*args, **kwargs)
        return None

    def find_field_and_fill(self, target, tag_title, tag_field, process):
        for name, value in inspect.getmembers(self.original):
            if not name.startswith('_'):
                if isinstance(value, (list, dict, set, tuple)):
                    for item in value:
                        if isinstance(item, dict) and target in item:
                            process(item[target])
                elif isinstance(value, dict) and target in value:
                    process(value[target])
                elif name == target:
                    process(value)

    def has_field(self, field_name):
        return hasattr(self.original, field_name)
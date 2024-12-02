import openpyxl


def column_number_to_text(column_number: int) -> str:
	return openpyxl.utils.get_column_letter(column_number)


def column_text_to_number(column_text: str) -> int:
	return openpyxl.utils.column_index_from_string(column_text)


if __name__ == "__main__":
	# Example usage
	print(column_number_to_text(1))  # Output: A
	print(column_text_to_number("A"))  # Output: 1

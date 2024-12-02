from typing import List, Dict

import openpyxl


class Reader:
    def __init__(self):
        self.err = None
        self.data = {}
        self.excel = None
        self.sheet_name = ""
        self.original_row = 1
        self.finished_row = 0
        self.title_row = 0
        self.titles = []

    def auto_read(self, filename: str) -> "Reader":
        return (
            self.open_file(filename)
            .set_original_row(2)
            .set_title_row(1)
            .set_sheet_name("Sheet1")
            .read_title()
            .read()
        )

    def auto_read_by_sheet_name(self, sheet_name: str, filename: str) -> "Reader":
        return (
            self.open_file(filename)
            .set_original_row(2)
            .set_title_row(1)
            .set_sheet_name(sheet_name)
            .read_title()
            .read()
        )

    def data_with_title(self) -> Dict[int, Dict[str, str]]:
        new_dict = {}
        for idx, value in self.data.items():
            new_dict[idx] = dict(zip(self.titles, value))
        return new_dict

    def set_data_by_row(self, row_number: int, data: List[str]) -> "Reader":
        self.data[row_number] = data
        return self

    def get_sheet_name(self) -> str:
        return self.sheet_name

    def set_sheet_name(self, sheet_name: str) -> "Reader":
        self.sheet_name = sheet_name
        return self

    def get_original_row(self) -> int:
        return self.original_row

    def set_original_row(self, original_row: int) -> "Reader":
        self.original_row = original_row - 1
        return self

    def get_finished_row(self) -> int:
        return self.finished_row

    def set_finished_row(self, finished_row: int) -> "Reader":
        self.finished_row = finished_row - 1
        return self

    def get_title_row(self) -> int:
        return self.title_row

    def set_title_row(self, title_row: int) -> "Reader":
        self.title_row = title_row - 1
        return self

    def get_title(self) -> List[str]:
        return self.titles

    def set_title(self, titles: List[str]) -> "Reader":
        if not titles:
            self.err = "Title cannot be empty"
            return self
        self.titles = titles
        return self

    def open_file(self, filename: str) -> "Reader":
        if not filename:
            self.err = "Filename cannot be empty"
            return self
        try:
            self.excel = openpyxl.load_workbook(filename)
        except Exception as e:
            self.err = f"Error opening file: {e}"
            return self
        self.set_title_row(1)
        self.set_original_row(2)
        self.data = {}
        return self

    def read_title(self) -> "Reader":
        if not self.get_sheet_name():
            self.err = "Sheet name is not set"
            return self
        try:
            sheet = self.excel[self.get_sheet_name()]
            self.set_title([cell.value for cell in sheet[self.get_title_row() + 1]])
        except Exception as e:
            self.err = f"Error reading title: {e}"
        return self

    def read(self) -> "Reader":
        if not self.get_sheet_name():
            self.err = "Sheet name is not set"
            return self
        try:
            sheet = self.excel[self.get_sheet_name()]
            rows = list(sheet.iter_rows(values_only=True))
            if self.finished_row == 0:
                for row_number, values in enumerate(
                    rows[self.get_original_row() :], start=self.get_original_row()
                ):
                    self.set_data_by_row(row_number, list(values))
            else:
                for row_number, values in enumerate(
                    rows[self.get_original_row() : self.get_finished_row()],
                    start=self.get_original_row(),
                ):
                    self.set_data_by_row(row_number, list(values))
        except Exception as e:
            self.err = f"Error reading data: {e}"
        return self

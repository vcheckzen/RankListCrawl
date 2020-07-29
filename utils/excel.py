from openpyxl import Workbook


class ExcelHelper:
    def __init__(self, excel_save_folder, excel_file_name):
        self.excel_file = excel_save_folder + excel_file_name + '.xlsx'
        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    def write_sheet_row(self, row_num, columns):
        for col_num, col_value in enumerate(columns):
            self.worksheet.cell(row_num, col_num + 1, col_value)

    def save(self):
        self.workbook.save(self.excel_file)
        self.workbook.close()

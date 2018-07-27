import xlrd
import xlwt

def read_excel():
    # 获取excel表格对象
    excel_obj = xlrd.open_workbook(r"E:\xiaoshou.xls")
    # 获取表格对象的所有工作簿名称，存放至列表中
    sheet_names = excel_obj.sheet_names()
    # 取到第一张工作簿
    sheet_name_obj = excel_obj.sheet_by_name("销售表")
    # 获取当前工作簿的总行数
    print(sheet_name_obj.nrows)
    # 循环获取每一行的数据
    for row in range(1,sheet_name_obj.nrows):
        row_data = sum(sheet_name_obj.row_values(row,2))
        print(row_data)

read_excel()
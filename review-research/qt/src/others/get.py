import openpyxl

workbook = openpyxl.load_workbook(filename = 'Qt_PredictionDataset.xlsx', use_iterators = True)
worksheet = workbook.get_sheet_by_name('Sheet1')
for row in worksheet.iter_rows():
	data = {
		'my_first_col':  row[0].value, # Column A
		'my_second_col': row[1].value, # Column B
		'my_third_col':  row[2].value, # Column C
	}
	print data['my_first_col'], '::', data['my_second_col'], '::', data['my_third_col']

from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
import services.stocks as stockService

def createSheet(stockSymbol, workbook):
	stock = stockService.Stock(stockSymbol)
	
	if hasattr(stock, "name") == False:
		return False
	
	stockData = stock.historicData.tz_localize(None)
	stockData = stockData.sort_index(ascending=False).reset_index()

	rows = stockData.shape[0]+1

	worksheet = workbook.create_sheet(stock.name)
	setColumnsStyle(worksheet)
	worksheet.column_dimensions["A"].width = 15

	i=0
	for r in dataframe_to_rows(stockData, index=False, header=True):
		worksheet.append(r)
		if r[0] != "Date":
			worksheet[f"A{i}"].number_format = 'dd/mm/yyyy;@'
		i+=1

	stockTable = Table(displayName=f"stockHistory{stockSymbol}", ref=f"A1:H{rows}")
	tableStyle = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
	stockTable.tableStyleInfo = tableStyle

	worksheet.add_table(stockTable)


def setColumnsStyle(worksheet):
	worksheet.column_dimensions["A"].width = 15
	worksheet.column_dimensions["B"].width = 15
	worksheet.column_dimensions["C"].width = 15
	worksheet.column_dimensions["D"].width = 15
	worksheet.column_dimensions["E"].width = 15
	worksheet.column_dimensions["F"].width = 15
	worksheet.column_dimensions["G"].width = 15
	worksheet.column_dimensions["H"].width = 15

if __name__ == "__main__":
	print('no tests')
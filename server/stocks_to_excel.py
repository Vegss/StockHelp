import openpyxl as xl
import services.sheets as sheetService
from datetime import datetime
import os
import sys
import json

def createWorkbook(stockSymbols, filename):
	if len(stockSymbols) == 0:
		return None
	if os.path.exists("updated.json"):
		with open("updated.json", "r") as f:
			info = json.load(f)
			if info["updated"] == datetime.now().strftime("%Y-%m-%d") and info["stocks"] == stockSymbols:
				print("Already updated today")
				os.system('powershell.exe /C ./stocks.xlsx')
				sys.exit()

	workbook = xl.Workbook()
	workbook.remove(workbook.active)

	for symbol in stockSymbols:
		sheetService.createSheet(symbol, workbook)

	try:
		workbook.save(f"{filename}.xlsx")
	except:
		return False

	info = {
		"updated": datetime.now().strftime("%Y-%m-%d"),
		"stocks": stockSymbols
	}

	with open("updated.json", "w") as outfile:
		json.dump(info, outfile)

if __name__ == "__main__":
	filename = "stocks"
	stockSymbols = ["ÖÖÖ"]
	if createWorkbook(stockSymbols, filename):
		os.system(f'powershell.exe /C ./{filename}.xlsx')
	print('No valid stocks.')
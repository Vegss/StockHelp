from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from stocks_to_excel import createWorkbook


app = FastAPI()

origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Stock(BaseModel):
    ticker: str

stocks = []

@app.get("/api/stocks", tags=["root"])
async def read_root() -> dict:
    global stocks
    return {"stocks": stocks}

@app.post("/api/stocks", tags=["root"], status_code=201)
async def post_root(stock: Stock) -> dict:
    global stocks
    stocks.append({"ticker": stock.ticker})
    return {"message": "success"}

@app.delete("/api/stocks/{ticker}", tags=["root"])
async def delete_root(ticker):
    global stocks
    stocks = [s for s in stocks if s['ticker'] != ticker]

@app.get("/api/stocks/download/{filename}", tags=["download"])
async def downloadStocks(filename):
    global stocks
    stockSymbols = [s['ticker'] for s in stocks]
    if createWorkbook(stockSymbols, filename) != False:
        file_path = os.path.join(f"{filename}.xlsx")
        stocks = []
        return FileResponse(path=file_path, filename=f"{filename}.xlsx")
    return { "message": "No stock found with given names." }
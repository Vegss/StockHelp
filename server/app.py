from flask import Flask, render_template, redirect, send_file, request
from stocks_to_excel import createWorkbook

app = Flask(__name__)

stocks = []

@app.route("/", methods=["GET", "POST"])
def index():
    print(stocks)
    return render_template("index.html", stocks=stocks)

@app.route("/addStocks", methods=["POST"])
def addStocks():
    stock = request.form['stock']
    stocks.append(stock)
    return redirect("/")

@app.route("/download", methods=["GET"])
def download():
    global stocks
    createWorkbook(stocks)
    stocks = []
    return send_file("stocks.xlsx", as_attachment=True)
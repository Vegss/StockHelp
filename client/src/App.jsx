import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [stocks, setStocks] = useState()
  const [ticker, setTicker] = useState('')
  const [filename, setFilename] = useState('')

  useEffect(() => {
    const getStocks = async () => {
      const response = await axios.get(`http://localhost:8000/api/stocks/`)
      setStocks(response.data.stocks)
    }
    getStocks()
  }, [])


  const addStock = async () => {
    setStocks(stocks.concat({ ticker: ticker }))
    setTicker('')
    await axios.post(`http://localhost:8000/api/stocks/`, { ticker: ticker })
  }

  const deleteStock = async (ticker) => {
    setStocks(stocks.filter((stock) => stock.ticker !== ticker))
    await axios.delete(`http://localhost:8000/api/stocks/${ticker}`)
  }

  const downloadExcel = async () => {
    if (filename === '') return alert('Please enter a filename')
    const link = document.createElement('a')
    link.href = `http://localhost:8000/api/stocks/download/${filename}`
    link.click()
    setFilename('')
    setStocks([])
  }

  if (!stocks) return <div>Loading...</div>

  return (
    <div className="App">
      <h1>StockHelp</h1>
      <p>Helps one to pick his stocks!</p>
      <div>
        <p>Ticker</p>
        <input type="text" placeholder='stock symbol' value={ticker} onChange={(e) => setTicker(e.target.value)} />
        <button onClick={addStock}>add</button>
        <p>Download as excel</p>
      </div>
      { 
        stocks.map((stock) => (
          <div key={stock.ticker}>
            <ul>
              <li>{stock.ticker}</li>
              <button onClick={() => deleteStock(stock.ticker)}>delete</button>
            </ul>
          </div>
          ))
      }
      <input type="text" placeholder='filename' value={filename} onChange={(e) => setFilename(e.target.value)} />
      <button onClick={downloadExcel}>Download</button>
      {/* <a onClick={() => setStocks([])} href='http://localhost:8000/api/stocks/download/${filename}'>download</a> */}
    </div>
  )
}

export default App

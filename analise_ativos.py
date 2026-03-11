import yfinance as yf

def dados_mercado(ticker):
    ativo = yf.Ticker(ticker)
    info = ativo.info

    return {
        "preco": info.get("currentPrice"),
        "lpa": info.get("trailingEps"),
        "book": info.get("bookValue"),
        "dividend": info.get("dividendYield")
    }
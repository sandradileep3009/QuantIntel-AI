import requests


def get_fundamental_price(ticker):

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "OVERVIEW",
        "symbol": ticker.upper(),
        "apikey": "92L0CH8ME7TA4GVI"
    }

    response = requests.get(url, params=params)

    data = response.json()

    # DEBUG
    print(data)

    # Check API errors
    if "Error Message" in data:
        print("Invalid ticker")
        return 0

    if "Note" in data:
        print("API limit reached")
        return 0


    print("Market Cap:", data.get("MarketCapitalization"))
    print("PE Ratio:", data.get("PERatio"))
    print("EPS:", data.get("EPS"))
    print("Revenue TTM:", data.get("RevenueTTM"))
    print("Profit Margin:", data.get("ProfitMargin"))


    fundamental_score = 0


    # Safe conversion function
    def safe_float(value):
        try:
            return float(value)
        except:
            return 0


    pe = safe_float(data.get("PERatio"))

    if 0 < pe < 25:
        fundamental_score += 2
    elif pe < 40:
        fundamental_score += 1


    profit_margin = safe_float(data.get("ProfitMargin"))

    if profit_margin > 0.15:
        fundamental_score += 2
    elif profit_margin > 0.05:
        fundamental_score += 1



    eps = safe_float(data.get("EPS"))

    if eps > 5:
        fundamental_score += 2
    elif eps > 0:
        fundamental_score += 1



    revenue_growth = safe_float(
        data.get("QuarterlyRevenueGrowthYOY")
    )


    if revenue_growth > 0.20:
        fundamental_score += 2
    elif revenue_growth > 0.05:
        fundamental_score += 1



    roe = safe_float(
        data.get("ReturnOnEquityTTM")
    )

    if roe > 0.15:
        fundamental_score += 2
    elif roe > 0.08:
        fundamental_score += 1



    de_ratio = safe_float(
        data.get("DebtToEquity")
    )

    if de_ratio < 1:
        fundamental_score += 2
    elif de_ratio < 2:
        fundamental_score += 1



    beta = safe_float(
        data.get("Beta")
    )

    if beta < 1.2:
        fundamental_score += 2
    elif beta < 1.8:
        fundamental_score += 1



    return fundamental_score
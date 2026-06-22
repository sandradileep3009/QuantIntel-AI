from fundamental import get_fundamental_price
from technical_score import get_technical_score
from sentiment_score import analyze_stock_news
from prediction_score import get_prediction_score
def get_final_score(ticker):
    fundamental_score=get_fundamental_price(ticker)
    technical_score = get_technical_score()
    sentiment_score=analyze_stock_news(ticker)
    prediction_score=get_prediction_score()

    investment_score = (fundamental_score+ technical_score+ sentiment_score+ prediction_score)
    if investment_score >= 13:
        recommendation = "BUY"

    elif investment_score >= 8:
        recommendation = "HOLD"

    else:
        recommendation = "SELL"
    return recommendation


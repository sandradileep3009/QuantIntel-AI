
from predictor import get_macd,get_rsi,get_signal,get_latest
def get_technical_score():
    latest_rsi = get_rsi()
    latest_macd = get_macd()
    latest_signal = get_signal()
    latest_volatility = get_latest()

    technical_score = 0

    if latest_macd > latest_signal:
        technical_score += 2

    if 40 <= latest_rsi <= 70:
        technical_score += 2

    if latest_volatility < 0.03:
        technical_score += 1

    return technical_score
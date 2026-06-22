from fundamental import get_fundamental_price
from technical_score import get_technical_score
from sentiment_score import analyze_stock_news
from predictor import predict_next_day
from report import generate_report
from predictor import run_prediction



ticker=input(
    "Enter stock ticker: "
).upper()



fundamental_score = get_fundamental_price(ticker)

predict_next_day()
technical_score = get_technical_score()


sentiment_score = analyze_stock_news(ticker)


predicted_price = run_prediction(ticker)


investment_score = (
    fundamental_score
    +
    technical_score
    +
    sentiment_score
)



if investment_score >= 13:

    recommendation="BUY"


elif investment_score >= 8:

    recommendation="HOLD"


else:

    recommendation="SELL"




print("\n===================")

print("Investment Score:",
      investment_score)

print("Recommendation:",
      recommendation)


print("===================")


recommendation = "HOLD"

upside = ((predicted_price - current_price) / current_price) * 100

if upside > 5 and sentiment > 0 and macd > 0:
    recommendation = "STRONG BUY"

elif upside > 2 and macd > 0:
    recommendation = "BUY"

elif upside < -5:
    recommendation = "STRONG SELL"

elif upside < -2:
    recommendation = "SELL"

    
report = generate_report(
    ticker,
    predicted_price,
    technical_score,
    sentiment_score,
    recommendation
)


print(report)
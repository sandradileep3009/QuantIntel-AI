
from google import genai
from google.genai.errors import ServerError
client = genai.Client(api_key="GCP_API_KEY")
def generate_report(
        ticker,
        current_price,
        predicted_price,
        macd,
        sentiment,
        recommendation
):

    prompt = f"""
You are a senior Wall Street equity research analyst.

Analyze the following stock.

Ticker: {ticker}

Current Price: {current_price}

Predicted Price: {predicted_price}

Expected Upside:
{((predicted_price-current_price)/current_price)*100:.2f}%

MACD:
{macd}

News Sentiment:
{sentiment}

Quantitative Recommendation:
{recommendation}

Create a detailed investment report.

Include:

1. Executive Summary

2. Buy / Hold / Sell Recommendation
- State recommendation clearly
- Confidence level

3. Technical Analysis
- MACD interpretation
- Momentum interpretation

4. Sentiment Analysis
- Explain effect of sentiment

5. AI Forecast Analysis
- Explain predicted move
- Bull case
- Bear case

6. Risk Factors

7. Investment Thesis

8. Final Verdict

Use professional hedge-fund style language.
"""


    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text


    except Exception as e:

        print("GEMINI ERROR:",e)

        return "AI Report unavailable"
import feedparser
from transformers import pipeline

def analyze_stock_news(ticker):
    pipe = pipeline("text-classification", model="ProsusAI/finbert")
    keyword = ticker.lower()

    rss_url = f'https://finance.yahoo.com/rss/headline?s={ticker}'

    feed=feedparser.parse(rss_url)

    if len(feed.entries) == 0:
        print("No news articles found.")
        exit()


    total_score=0
    no_of_entries=0

    for i,entry in enumerate(feed.entries):
        if keyword.lower() not in entry.summary.lower():
            continue 
        print("Title: ",entry.title)
        print("Link: ",entry.link)
        print("Published: ",entry.published)
        print("Summary: ",entry.summary)

        sentiment=pipe(entry.summary)[0]
        print("Label: ",sentiment["label"],"\n Scores: ",sentiment["score"])
        print("-" * 40)

        if sentiment["label"].lower()=="positive":
            total_score+=sentiment["score"]
            no_of_entries+=1
            
        elif sentiment["label"].lower()=="negative":
            total_score-=sentiment["score"]
            no_of_entries+=1
        

    final_rating=total_score/no_of_entries

    print("The final rating is: ",final_rating)

    if final_rating>=0.15:
        print("Positive impact")
    elif final_rating<=-0.15:
        print("Negative impact")
    else:
        print("Neutral")

    print("\n===== FINAL REPORT =====")
    print(f"Ticker: {ticker}")
    print(f"Articles Analyzed: {no_of_entries}")
    print(f"Sentiment Score: {final_rating:.4f}")
    sentiment_score = 0
    if final_rating > 0.25:
        sentiment_score = 3
    elif final_rating > 0:
        sentiment_score = 2
    elif final_rating > -0.25:
        sentiment_score = 1
    else:
        sentiment_score = 0
    return sentiment_score




def get_sentiment_score(ticker):
    return analyze_stock_news(ticker)

import pandas as pd

def get_prediction_score():# Load CSV
    df = pd.read_csv("predictions.csv")

    # Get latest row
    latest_actual = df["Actual"].iloc[-1]
    latest_predicted = df["Predicted"].iloc[-1]

    # Calculate upside percentage
    upside = (
        (latest_predicted - latest_actual)
        / latest_actual
    ) * 100

    # Prediction score
    if upside > 10:
        prediction_score = 3
    elif upside > 5:
        prediction_score = 2
    elif upside > 0:
        prediction_score = 1
    else:
        prediction_score = 0

    return prediction_score
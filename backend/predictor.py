# predictor.py

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.layers import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


# store results here
prediction_results = {}


def run_prediction(ticker):
    global prediction_results


    # =========================
    # LOAD DATA
    # =========================

    df = pd.read_csv("Stock_price.csv")

    print("Original Shape:", df.shape)
    print(df.head())


    # =========================
    # CLEAN DATA
    # =========================

    df.columns = [
        "DATE",
        "OPEN",
        "HIGH",
        "LOW",
        "CLOSE",
        "VOLUME"
    ]


    numeric_cols = [
        "OPEN",
        "HIGH",
        "LOW",
        "CLOSE",
        "VOLUME"
    ]


    for col in numeric_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    df = df.dropna(
        subset=["CLOSE"]
    )

    df = df.sort_values("DATE")



    # =========================
    # FEATURES
    # =========================


    df["RETURN"] = (
        df["CLOSE"].pct_change()
    )


    df["MA5"] = (
        df["CLOSE"]
        .rolling(5)
        .mean()
    )


    df["MA20"] = (
        df["CLOSE"]
        .rolling(20)
        .mean()
    )


    df["VOLATILITY"] = (
        df["RETURN"]
        .rolling(20)
        .std()
    )


    # RSI

    delta = df["CLOSE"].diff()

    gain = delta.where(
        delta > 0,
        0
    )

    loss = -delta.where(
        delta < 0,
        0
    )


    avg_gain = (
        gain
        .rolling(14)
        .mean()
    )


    avg_loss = (
        loss
        .rolling(14)
        .mean()
    )


    rs = avg_gain / avg_loss


    df["RSI"] = (
        100 -
        (100/(1+rs))
    )


    # MACD

    ema12 = (
        df["CLOSE"]
        .ewm(
            span=12,
            adjust=False
        )
        .mean()
    )


    ema26 = (
        df["CLOSE"]
        .ewm(
            span=26,
            adjust=False
        )
        .mean()
    )


    df["MACD"] = ema12 - ema26


    df["MACD_SIGNAL"] = (
        df["MACD"]
        .ewm(
            span=9,
            adjust=False
        )
        .mean()
    )


    df=df.dropna()



    # =========================
    # LINEAR REGRESSION
    # =========================


    features = [

        "CLOSE",
        "VOLUME",
        "MA5",
        "MA20",
        "RETURN",
        "VOLATILITY",
        "RSI",
        "MACD",
        "HIGH",
        "LOW"

    ]


    data=df[features]


    X=[]
    y=[]

    window=5


    for i in range(
        len(data)-window
    ):

        X.append(
            data.iloc[
                i:i+window
            ].values.flatten()
        )

        y.append(
            data.iloc[
                i+window
            ]["CLOSE"]
        )


    X=np.array(X)
    y=np.array(y)


    split=int(
        len(X)*0.8
    )


    x_train=X[:split]
    x_test=X[split:]

    y_train=y[:split]
    y_test=y[split:]



    lr_model = LinearRegression()


    lr_model.fit(
        x_train,
        y_train
    )


    lr_pred = lr_model.predict(
        x_test
    )


    print(
        "Linear MAE:",
        mean_absolute_error(
            y_test,
            lr_pred
        )
    )



    pd.DataFrame({

        "Actual":y_test,
        "Predicted":lr_pred

    }).to_csv(
        "predictions.csv",
        index=False
    )



    # =========================
    # LSTM
    # =========================


    lstm_features=[

        "CLOSE",
        "VOLUME",
        "MA5",
        "MA20",
        "RETURN",
        "HIGH",
        "LOW"

    ]


    lstm_data=df[lstm_features]


    scaler=MinMaxScaler()


    scaled=scaler.fit_transform(
        lstm_data
    )


    X_lstm=[]
    y_lstm=[]


    window=60


    for i in range(
        window,
        len(scaled)
    ):

        X_lstm.append(
            scaled[
                i-window:i
            ]
        )


        y_lstm.append(
            scaled[i,0]
        )



    X_lstm=np.array(
        X_lstm
    )


    y_lstm=np.array(
        y_lstm
    )


    split=int(
        len(X_lstm)*0.8
    )


    X_train=X_lstm[:split]
    X_test=X_lstm[split:]


    y_train=y_lstm[:split]
    y_test=y_lstm[split:]



    model = Sequential([


        Input(
            shape=(
                window,
                len(lstm_features)
            )
        ),


        LSTM(
            64,
            return_sequences=True
        ),


        Dropout(0.2),


        LSTM(64),


        Dropout(0.2),


        Dense(25),


        Dense(1)

    ])



    model.compile(

        optimizer="adam",

        loss="mse"

    )



    print(
        "Training LSTM..."
    )


    model.fit(

        X_train,
        y_train,

        epochs=20,

        batch_size=16,

        verbose=1

    )



    model.save(
        "stock_lstm_model.keras"
    )



    # =========================
    # NEXT DAY PREDICTION
    # =========================


    last60 = scaled[-60:]


    input_data = last60.reshape(

        1,
        60,
        len(lstm_features)

    )


    prediction = model.predict(
        input_data
    )


    dummy=np.zeros(

        (
            1,
            len(lstm_features)
        )

    )


    dummy[0,0]=prediction[0][0]


    final_price = scaler.inverse_transform(
        dummy
    )[0,0]



    print(
        "Tomorrow predicted CLOSE:",
        final_price
    )
    
    current_price = df["CLOSE"].iloc[-1]

    change_pct = (
        (final_price - current_price)
        / current_price
    ) * 100

    if change_pct > 1:
        recommendation = "BUY"

    elif change_pct < -1:
        recommendation = "SELL"

    else:
        recommendation = "HOLD"


    prediction_results = {

        "current_price":
        float(df["CLOSE"].iloc[-1]),

        "predicted_price":
        float(final_price),

        "rsi":
        float(df["RSI"].iloc[-1]),

        "macd":
        float(df["MACD"].iloc[-1]),

        "signal":
        float(df["MACD_SIGNAL"].iloc[-1]),

        "volatility":
        float(df["VOLATILITY"].iloc[-1]),

        "recommendation":
        recommendation
    }
    return prediction_results


def get_current_price():

    return prediction_results["current_price"]



def get_price():

    return prediction_results["predicted_price"]



def get_rsi():

    return prediction_results.get("rsi",0)



def get_macd():

    return prediction_results.get("macd",0)



def get_signal():

    return prediction_results.get("signal",0)



def get_latest():

    return prediction_results.get("volatility",0)



# backwards compatibility
predict_next_day = run_prediction
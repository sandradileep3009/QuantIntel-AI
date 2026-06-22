from fastapi import FastAPI
from predictor import run_prediction
from data_retrievel import create_data
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/analyze/{ticker}")
def analyze(ticker: str):

    try:

        success = create_data(ticker)

        if not success:
            return {
                "status": "failed",
                "error": "Failed to download stock data"
            }

        result = run_prediction(ticker)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }
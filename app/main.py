import pickle
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST  # NUOVO

# Caricamento del modello
filename = "model/sentiment_analysis_model.pkl"
loaded_pipeline = pickle.load(open(filename, "rb"))

app = FastAPI()

# Metriche
REQUEST_TIME = Histogram("predict_request_seconds", "Tempo di risposta delle richieste a /predict")
PREDICTION_ERRORS = Counter("predict_errors_total", "Numero di errori di predizione")


# Formato della richiesta: {"review": "..."}
class Review(BaseModel):
    review: str


@app.post("/predict")
def predict(data: Review):
    with REQUEST_TIME.time():  # misura il tempo di risposta
        try:
            # Testo da prevedere (lista di stringhe)
            text_to_predict = [data.review]

            # Previsione
            sentiment = loaded_pipeline.predict(text_to_predict)[0]
            confidence = loaded_pipeline.predict_proba(text_to_predict)[0].max()

            return {"sentiment": str(sentiment), "confidence": round(float(confidence), 2)}
        except Exception:
            PREDICTION_ERRORS.inc()  # conta l'errore
            raise HTTPException(status_code=500, detail="Errore di predizione")


# Endpoint per Prometheus
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
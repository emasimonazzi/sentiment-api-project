# Immagine di partenza: Linux leggero con Python già installato
FROM python:3.13-slim

# Cartella di lavoro dentro il container
WORKDIR /app

# Installa le librerie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice, il modello e i test
COPY app/ app/
COPY model/ model/
COPY tests/ tests/

# Porta su cui risponde l'API
EXPOSE 8000

# Comando che avvia l'API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
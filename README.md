# Sentiment Analysis API – Deploy e Monitoraggio

API per l'analisi del sentiment di recensioni in inglese (`positive`, `negative`, `neutral`), con pipeline CI/CD Jenkins e monitoraggio Prometheus + Grafana.

Repository: https://github.com/emasimonazzi/sentiment-api-project

Ho reso disponibile il modello di Sentiment Analysis (scikit-learn) tramite un’API FastAPI con gli endpoint /predict e /metrics, verificata da unit test e test di integrazione e containerizzata con Docker.
Una pipeline Jenkins si avvia a ogni commit su GitHub ed esegue build, test, deploy con Docker Compose e smoke test; il deploy avviene solo se tutti i test passano e alla fine arriva una notifica di successo o di errore.
Prometheus raccoglie tempo di risposta, errori, CPU e memoria, e Grafana li mostra in tempo reale in una dashboard come da requisito che si carica da sola all’avvio.

## Stack

FastAPI · scikit-learn · Docker Compose · Jenkins · Prometheus · Grafana

## Avvio

```bash
docker compose up -d --build
```

| Servizio | Indirizzo |
|---|---|
| API | http://127.0.0.1:8000/docs |
| Prometheus | http://127.0.0.1:9090 |
| Grafana (admin/admin) | http://127.0.0.1:3000 |

## Test

```bash
docker run --rm sentiment-api python -m pytest -v
```
Unit test sul modello (`test_model.py`) e test di integrazione sull'API (`test_api.py`).

## Jenkins

```bash
docker build -t my-jenkins ./jenkins
docker run -d --name jenkins -p 127.0.0.1:8080:8080 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock my-jenkins
```
Job di tipo Pipeline → *Pipeline script from SCM* → questo repository, branch `*/main`.

Pipeline: **Trigger** (ogni 2 min) → **Build** → **Test** → **Deploy** → **test** → **Notifica**. Se un test fallisce, il deploy non avviene.

## Scelte progettuali

- **Test eseguiti nell'immagine Docker**: si verifica esattamente ciò che va in produzione.
- **Config di Prometheus e Grafana copiate nelle immagini** 
- **Datasource e dashboard Grafana in provisioning**: si caricano da sole all'avvio.
- **Polling invece del webhook**: Jenkins è locale e non raggiungibile da GitHub.
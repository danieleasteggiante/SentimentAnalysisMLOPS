# Sentiment Analysis MLOps

<img width="931" height="691" alt="MLOPS_project drawio" src="https://github.com/user-attachments/assets/c7d65cf4-e597-4e33-bf50-28f62397adaf" />





Sistema di analisi del sentiment con architettura a microservizi orchestrata con `docker-compose`. Tutti i servizi girano su un server tramite `docker-compose up -d`.

Questo progetto è una pipeline MLOps per l'analisi del sentiment che mette insieme interfaccia utente, automazione del training e deployment dei modelli in produzione. Gli utenti inviano testi tramite la web app e possono fornire feedback; il backoffice permette di gestire i dataset e avviare training manuali; il trainer esegue il fine tuning e aggiorna il model server che serve le inferenze; Grafana monitora le performance e invia alert se la qualità cala; il database PostgreSQL conserva predizioni, feedback e metadati. Il sistema è pensato per girare su un singolo server con docker compose, comunicare via nomi di servizio e essere esposto in modo sicuro tramite reverse proxy e TLS. Per provare rapidamente: esegui docker compose up -d e usa gli endpoint descritti nel README.

L'indirizzo IP o dominio del server VPS dove gira il sistema è indicato come `<HOST>`.
Il valore `<HOST>` reale é 76.13.8.56 
Quindi per esempio l'endpoint di inferenza via web app sarà `http://76.13.8.56:8000/static/index`.


## Panoramica componenti

- Web App (UI + API) — porta `8000`
  - UI principale: `GET /` \(serve `static/index`\)
  - API inferenza: `POST /api/predict` — body JSON: `{ "text": "..." }`
  - API feedback: `POST /api/feedback` — body JSON: `{ "prediction_id": "...", "feedback": "positive|negative|neutral", "note": "..." }`
  - Health: `GET /health`

- Backoffice (UI per dataset e training) — porta `8502`
  - UI backoffice: `GET /backoffice/index`
  - Avvio training manuale: `POST /backoffice/api/train` — opzionale payload per parametri di training

- Model (Model Server, API di inferenza) — porta `8501`
  - Scarica e serve il modello corretto (cache + caricamento automatico)
  - Endpoint inferenza: `POST /predict` — body JSON: `{ "text": "..." }`

- Trainer (servizio di fine-tuning e redeploy) — porta `8502`
  - Scarica modello base da Hugging Face, esegue fine-tuning, aggiorna DB e triggera il redeploy del `model`
  - Avvia training: `POST /train` — body JSON con dataset/config

- Grafana (monitoring & alerting) — porta `3000`
  - Dashboard per performance e feedback
  - Alert via e\-mail se il modello sotto\-performante
  - Credenziali iniziali: admin / admin

- DB (PostgreSQL) — porta host `5555`, porta container `5432`
  - Schema `prediction` usato da tutti i componenti per predizioni, feedback e metadata di training
  - Persistenza tramite volume `db_data`

## Endpoints rapidi (esempi curl)

- Inferenza via Web App (proxy verso `model` o direttamente)
  - curl -X POST http://<HOST>:8000/api/predict -H "Content-Type: application/json" -d '{"text":"ottimo prodotto"}'

- Inferenza diretta sul Model Server
  - curl -X POST http://<HOST>:8501/predict -H "Content-Type: application/json" -d '{"text":"ottimo prodotto"}'

- Inviare feedback
  - curl -X POST http://<HOST>:8000/api/feedback -H "Content-Type: application/json" -d '{"prediction_id":"123","feedback":"negative","note":"falso positivo"}'

- Avviare training dal Backoffice
  - curl -X POST http://<HOST>:8001/backoffice/api/train -H "Content-Type: application/json" -d '{"dataset_id":"v1"}'

## Volumi e persistenza

- `db_data` — dati PostgreSQL
- `grafana_data` — config e dashboard Grafana
- eventuali cache modello (`hf-cache`) montate per evitare download ripetuti

## Docker / Avvio

- Avvia tutto:
  - `docker compose up -d`
- Stato container:
  - `docker compose ps`
- Log:
  - `docker compose logs -f`

## Grafana / Datasource

- Al primo accesso in Grafana:
  - Host datasource PostgreSQL (interno): `db:5432`
  - Database: `prediction`
  - User: `admin`
  - Password: `admin`
  - SSL Mode: `disable`

## CI/CD (pipeline sintetica)

- Workflow attivato su ogni push su repository (esempio GitHub Actions):
  - Step 1: Esegui test unitari e di integrazione per la `web_app`
    - comando: `python -m pytest web_app/tests/ -v`
  - Step 2: Se il messaggio del commit contiene la parola chiave `deploy` viene eseguito il job di deploy:
    - esempio action: connettersi via SSH al server e lanciare:
      - `docker compose pull`
      - `docker compose up -d --remove-orphans`
  - Nota: il deploy automatico richiede chiavi SSH, segreti e permessi adeguati sul server.

## Note operative

- Assicurarsi che le versioni dei container siano compatibili prima del restore di volumi (es. `grafana_data`)
- Se i servizi comunicano via DNS interno (`trainer`, `model`, `db`) usare i nomi dei servizi nel `docker-compose` (es. `http://model:8501`)
- Per esposizione pubblica: usare reverse proxy (traefik/nginx) + TLS e aprire porte sul firewall del VPS (`ufw`/security group)

## Contatti / Troubleshooting rapido

- Verificare logs:
  - `docker compose logs -f <service>`
- Controllare porte d'ascolto:
  - `ss -tulpn | grep LISTEN`

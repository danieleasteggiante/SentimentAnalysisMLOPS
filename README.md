# Sentiment Analysis MLOps

Sistema di analisi del sentiment con architettura a microservizi che include inferenza ML, raccolta feedback e monitoraggio delle performance.

## 🏗️ Architettura

Il progetto è composto da 4 componenti principali orchestrati con Docker Compose:

### 1. **Web App (FastAPI)** 
- **Porta**: `8000`
- **Tecnologia**: FastAPI
- **Funzioni**:
  - Interfaccia web per l'analisi del sentiment
  - API REST per richieste di inferenza
  - Raccolta e registrazione del feedback degli utenti
  - Persistenza dei dati su PostgreSQL

### 2. **Model Server**
- **Porta**: `8501`
- **Funzioni**:
  - Download automatico del modello di ML da Hugging Face
  - Esposizione API per l'inferenza del sentiment
  - Cache del modello per performance ottimali
  - Comunicazione con il database per logging delle predizioni

### 3. **PostgreSQL Database**
- **Porta**: `5555`
- **Tecnologia**: PostgreSQL 15
- **Funzioni**:
  - Persistenza delle predizioni
  - Storage del feedback degli utenti
  - Metriche per l'analisi delle performance
  - Inizializzazione automatica dello schema via `initdb`

### 4. **Grafana (Monitoring & Observability)**
- **Porta**: `3000`
- **Tecnologia**: Grafana
- **Funzioni**:
  - Connessione diretta al database PostgreSQL
  - Dashboard per monitoraggio real-time delle predizioni
  - Analisi delle performance del modello
  - Visualizzazione dei feedback degli utenti
  - Metriche di utilizzo del sistema

## 🚀 Quick Start

### Prerequisiti
- Docker
- Docker Compose

### Avvio del sistema

```bash
# Clone del repository
git clone https://github.com/danieleasteggiante/SentimentAnalysisMLOPS.git
cd SentimentAnalysisMLOPS

# Avvio di tutti i servizi
docker-compose up -d

# Verifica dello stato dei container
docker-compose ps

# Visualizza i log
docker-compose logs -f
```

### Accesso ai servizi

- **Web App**: http://localhost:8000
- **Model Server API**: http://localhost:8501
- **Grafana Dashboard**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`
- **PostgreSQL**: `localhost:5555`
  - Database: `prediction`
  - User: `admin`
  - Password: `admin`

## 📊 Configurazione Grafana

Al primo accesso a Grafana:

1. Login con credenziali `admin/admin`
2. Il datasource PostgreSQL va configurato manualmente:
   - **Host**: `db:5432`
   - **Database**: `prediction`
   - **User**: `admin`
   - **Password**: `admin`
   - **SSL Mode**: `disable`

Le configurazioni verranno salvate nel volume `grafana_data` e persistono tra i riavvii.

## 🧪 Testing

```bash
# Esegui i test
python -m pytest web_app/tests/ -v

# Test
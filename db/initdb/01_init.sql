CREATE TABLE IF NOT EXISTS model_versions (
  id SERIAL PRIMARY KEY,
  model_name TEXT NOT NULL,
  version INTEGER NOT NULL,
  registration_date TIMESTAMP DEFAULT now()
);

INSERT INTO model_versions (model_name, version, registration_date)
VALUES ('danieleasteggiante/sentiment-analysis-model', 'v0.1.0', now());

CREATE TABLE IF NOT EXISTS prediction_evaluation (
  id SERIAL PRIMARY KEY,
  message_text TEXT NOT NULL,
  prediction TEXT NOT NULL,
  evaluation TEXT NOT NULL,
  time_stamp TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feedbacks (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  message_text TEXT NOT NULL,
  feedback_result TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS start_training_logs (
  id SERIAL PRIMARY KEY,
  feedback_id TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);
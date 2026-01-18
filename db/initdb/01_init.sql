CREATE TABLE IF NOT EXISTS model_versions (
  id SERIAL PRIMARY KEY,
  model_name TEXT NOT NULL,
  version INTEGER,
  registration_date TIMESTAMP DEFAULT now()
);

INSERT INTO model_versions (model_name, version, registration_date)
VALUES ('cardiffnlp/twitter-roberta-base-sentiment-latest', null, now());

CREATE TABLE IF NOT EXISTS prediction_evaluation (
  id SERIAL PRIMARY KEY,
  message_text TEXT NOT NULL,
  prediction TEXT NOT NULL,
  evaluation TEXT NOT NULL,
  time_stamp TIMESTAMP DEFAULT now()
);
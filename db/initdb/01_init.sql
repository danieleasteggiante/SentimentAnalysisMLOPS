CREATE TABLE IF NOT EXISTS model_versions (
  id SERIAL PRIMARY KEY,
  model_name TEXT NOT NULL,
  version TEXT NOT NULL,
  registration_date TIMESTAMP DEFAULT now()
);

INSERT INTO model_versions (model_name, version, registration_date)
VALUES ('danieleasteggiante/sentiment-analysis-model', 'v0.1.0', now());


CREATE TABLE IF NOT EXISTS feedbacks (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  message_text TEXT NOT NULL,
  labels TEXT NOT NULL,
  feedback_result TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

INSERT INTO feedbacks (username, message_text, labels, feedback_result, created_at)
VALUES ('test_user', 'I love this product!', 'positive', 'LIKE', now()),
       ('test_user2', 'This is the worst service ever.', 'negative', 'LIKE', now()),
       ('test_user3', 'It is okay, not great but not terrible.', 'neutral', 'LIKE', now()),
       ('test_user4', 'I am extremely satisfied with my experience.', 'positive', 'LIKE', now()),
       ('test_user5', 'I will never use this again.', 'negative', 'LIKE', now()),
       ('test_user6', 'The product is average, nothing special.', 'neutral', 'LIKE', now()),
       ('test_user7', 'Absolutely fantastic! Exceeded my expectations.', 'positive', 'LIKE', now()),
       ('test_user8', 'Totally disappointed, it broke after one use.', 'negative', 'LIKE', now()),
       ('test_user9', 'Mediocre at best, could be improved.', 'neutral', 'LIKE', now()),
       ('test_user10', 'I am thrilled with my purchase!', 'positive', 'LIKE', now()),
       ('test_user11', 'This is a complete waste of money.', 'negative', 'LIKE', now()),
       ('test_user12', 'It works fine, nothing extraordinary.', 'neutral', 'LIKE', now()),
       ('test_user13', 'Exceeded all my expectations!', 'positive', 'LIKE', now()),
       ('test_user14', 'Very unhappy with the quality.', 'negative', 'LIKE', now()),
       ('test_user15', 'Just an average experience overall.', 'neutral', 'LIKE', now()),
       ('test_user16', 'I am delighted with the results!', 'positive', 'LIKE', now()),
       ('test_user17', 'Extremely dissatisfied, will not recommend.', 'negative', 'LIKE', now()),
       ('test_user18', 'It is neither good nor bad.', 'neutral', 'LIKE', now());


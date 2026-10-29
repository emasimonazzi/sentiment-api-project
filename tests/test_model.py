import pickle

# Carica il modello
filename = "model/sentiment_analysis_model.pkl"
loaded_pipeline = pickle.load(open(filename, "rb"))

# test corretto funzionamento del modello
def test_modello_ha_le_classi_giuste():
    assert list(loaded_pipeline.classes_) == ["negative", "neutral", "positive"]


def test_recensione_positiva():
    text_to_predict = ["This product is amazing! I love it."]
    assert loaded_pipeline.predict(text_to_predict)[0] == "positive"


def test_recensione_negativa():
    text_to_predict = ["Terrible quality, it broke after one day."]
    assert loaded_pipeline.predict(text_to_predict)[0] == "negative"


def test_recensione_neutra():
    text_to_predict = ["It's okay, nothing special."]
    assert loaded_pipeline.predict(text_to_predict)[0] == "neutral"


def test_probabilita_sommano_a_uno():
    text_to_predict = ["This product is amazing! I love it."]
    probabilita = loaded_pipeline.predict_proba(text_to_predict)[0]
    assert round(sum(probabilita), 2) == 1.0
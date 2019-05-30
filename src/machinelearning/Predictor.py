import joblib
from src.machinelearning import DataLoader
from src.mongoDB import Fetcher


class Predictor:

    def __init__(self):
        self.load_model = joblib.load('./machinelearning/prediction_model.sav')

    def predict(self, id):
        fetcher = Fetcher()
        load_model = joblib.load('./machinelearning/prediction_model.sav')
        tweet = fetcher.get_tweet(id)
        prediction = load_model.predict(tweet['full_text'])
        prob = load_model.predict_proba(tweet['full_text'])
        answ = {}
        if prediction[0] == 'True':
            answ['description'] = 'ML model DO NOT classify this as a Fake News.'
        else:
            answ['description'] = 'ML model classify this as a Fake News.'
        answ['probability'] = prob[0][0]
	
        return (answ)




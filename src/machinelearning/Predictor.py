import joblib
from src.machinelearning import DataLoader



class Predictor:

    def __init__(self):
        self.load_model = joblib.load('./machinelearning/prediction_model.sav')

    def predict(self, var):
        load_model = joblib.load('./machinelearning/prediction_model.sav')

        prediction = load_model.predict(DataLoader.stem(var))
        prob = load_model.predict_proba(DataLoader.stem(var))
        answ = {}
        if prediction[0] == 'True':
            answ['description'] = 'ML model DO NOT classify this as a Fake News.'
        else:
            answ['description'] = 'ML model classify this as a Fake News.'
        answ['probability'] = prob[0][0]
	
        return (answ)




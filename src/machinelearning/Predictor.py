import joblib
import DataLoader


class Predictor:

    def __init__(self):
        self.load_model = joblib.load('prediction_model.sav')
    def predict(self, var):
        load_model = joblib.load('prediction_model.sav')

        prediction = load_model.predict(DataLoader.stem(var))
        prob = load_model.predict_proba(DataLoader.stem(var))

        return ((prediction[0],prob[0][1]))


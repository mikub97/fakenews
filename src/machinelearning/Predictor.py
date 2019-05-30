import joblib
import DataLoader


#function to run for prediction
def predict(var):
#retrieving the best model for prediction call
    load_model = joblib.load('prediction_model.sav')

    prediction = load_model.predict(DataLoader.stem(var))
    prob = load_model.predict_proba(DataLoader.stem(var))

    return ((prediction[0],prob[0][1]))


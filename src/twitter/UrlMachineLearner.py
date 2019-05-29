import pandas as pd
import numpy as np
import random
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class UrlMachineLearner:
    def __init__(self):
        self.url = 'data.csv'

    def sanitization(self, web):  # tokenizing method
        web = web.lower()
        token = []
        dot_token_slash = []
        raw_slash = str(web).split('/')
        for i in raw_slash:
            raw1 = str(i).split('-')  # removing slash to get token
            slash_token = []
            for j in range(0, len(raw1)):
                raw2 = str(raw1[j]).split('.')  # removing dot to get the tokens
                slash_token = slash_token + raw2
            dot_token_slash = dot_token_slash + raw1 + slash_token  # all tokens
        token = list(set(dot_token_slash))  # to remove same words
        if 'com' in token:
            token.remove('com')  # remove com
        return token

    def is_url_malicious(self, link):

        url_csv = pd.read_csv(self.url, ',', error_bad_lines=False)
        url_df = pd.DataFrame(url_csv)  # to convert into data frames
        url_df = np.array(url_df)  # to convert into array
        random.shuffle(url_df)
        y = [d[1] for d in url_df]  # all labels
        urls = [d[0] for d in url_df]  # all urls corresponding to a label {G/B}
        # http://blog.christianperone.com/2011/09/machine-learning-text-feature-extraction-tf-idf-part-i/

        vectorizer = TfidfVectorizer(tokenizer=self.sanitization)  # term-frequency and inverse-document-frequency
        x = vectorizer.fit_transform(urls)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        lgr = LogisticRegression()  # Logistic regression
        lgr.fit(x_train, y_train)
        score = lgr.score(x_test, y_test)
        vectorizer_save = vectorizer

        x_predict = [link]
        x_predict = vectorizer.transform(x_predict)
        y_predict = lgr.predict(x_predict)

        if y_predict[0] == 'bad':
            return True

        return False


if __name__ == '__main__':
    obj = UrlMachineLearner()
    print(obj.is_url_malicious('aszdziennik.pl'))







#fakenews

##Api do twittera
+ W klasie TwitterConnection jest metoda dzieki ktorej mam dostep do api twittera
poprzez biblioteke tweety

+ Do uruchomienia jej potrzebujemy pliku twitter-credentials.json ktora wylse wam na FB

+ Do gitignore dalem pliki json jeszcze zeby ten plik nie commitowal sie bo to sa dane do mojego(bielas) konta

##inne

Wrzuciłem książkę violent python  w której jest coś tam o czytaniu tweetów ( może być już nieaktualne co do tego ) oraz parsowaniu stronek z użyciem beautyful soup. Myślę, że z tego skorzystamy.

Podzieliłbym projekt na 4 części

1. Zebranie danych do uczenia nadzorowanego + wytrenowanie odpowiedniego modelu

2. Znalezienie sposobu na "potwierdzenie" newsa, tzn. zweryfikowanie go przeszukując internet

3. Połączenie wyniku z 1 i 2 oraz wypracowanie odpowiedzi na pytanie fake or not ?

4. Testy


Przydatne linki : 
- PageRank extractor -> https://github.com/aablack/websearchapp/blob/master/search/rank_provider.py 

- projket w pythonie -> https://github.com/nishitpatel01/Fake_News_Detection

- https://data.world/d1gi/11000-expanded-labeled-links-from-365k-troll-tweets

- https://www.pantechsolutions.net/fake-news-detection-using-machine-learning

- https://towardsdatascience.com/i-built-a-fake-news-detector-using-natural-language-processing-and-classification-models-da180338860e

- https://www.geeksforgeeks.org/project-idea-know-more/

- https://github.com/cvhariharan/fake-news-detector

-  countvectorizer -> https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/

Dane :

- https://www.kaggle.com/mrisdal/fake-news

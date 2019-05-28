#fakenews

##Api do twittera
W klasie TwitterConnection jest atrybut api do twittera poprzez biblioteke tweepy

+ Do uruchomienia jej potrzebujemy pliku twitter-credentials.json ktora wylse wam na FB. Wsadzamy go do /resources/

+ Do gitignore dalem pliki json jeszcze zeby ten plik nie commitowal sie bo to sa dane do mojego(bielas) konta

Dokumentacja ( link umożliwia tylko wyświetlanie, więc podajcie maile to was dodam do edycji ) :
https://docs.google.com/document/d/1WuP45YpfjxqyZbNAFnbzWICVt7ftB1hCSw-E8Wq9o8w/edit?usp=sharing

##Bielas 28.05.2019
UWAGA!
- zeby moj modul zadzial przy wyszukiwaniu tweetow musz byc ustawione parametry:
    - tweet_mode='extended',
    - include_entities=True

dodalem:
- klasa BotChecker
- klasa UrlMachineLearner
- plik data.csv

Klasa UrlMachineLearner sprawdza czy dany link jest wiarygodny - uczy sie na podstwie
danych uczacych w 'data.csv' - nie jest to niestety bardzo dokladne przez co moze wypluwac wiele fake'owych tweetow

klasa BotChecker sprawdza czy dany tweet jest fake na podstawie:

- Czy dany uzytkownik jest botem - jesli roznica czasu miedzy dwoma 
opublikowanymi tweetami jest wieksza niz dwa dni to znaczy ze to jest bot

- na podstawie wiarygodnosci URLi w treści tweeta - tutaj wykorzystywane sa dwie metody
jesli wlaczy sie UrlMachineLearner to program uczy sie sprawdzac czy link jest ok,
jesly sie to wyłączy to program sprawdza kod HTTP danego url, jesli jest nie tak to znaczy
ze tweet jest fake'owy

UWAGA:

jesli korzystami z klasy BotChecker to tylko z metod:
- is_fake_based_on_user(self, tweet) - sprawdzanie bota, domyslnie wlaczone machine learning
- is_fake_based_on_external_urls(self, tweet) - domyslnie wlaczone machine learning
- is_fake(self, tweet, isMachineLearnignOn) - tutaj wlaczamy machine learning podajac jako
drugi argument True, wylaczamy podajac False

Dodatkowo dzieki klasie mozemy sprawdzic sentyment danego tweeta:
- get_tweet_sentiment(self, tweet) - wypluwa nam: positive, negative, neutral

Plik BotChecker mozna opdalic dla celow testowych

Co moze zostac ulepszone:
- cos sie pieprzylo z importami wiec wszytkie pliki dalem do jednej paczki,
jak ogarniacie lepiej pythona to mozecie zrefactorowac



##Inna sekcja

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

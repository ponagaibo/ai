from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import re

class clasificator:
    def classify(self, input_file, output_file):
        df = pd.read_csv(input_file)
        df.columns = ['Id', 'OwnerUserId', 'CreationDate', 'ParentId', 'Score', 'IsAcceptedAnswer', 'Body']
        df['Class'] = np.sign(df['Score'])
        print("Whole size: " + str(len(df)))

        i = 0
        while i < len(df['Body']):
            if df['Class'][i] <= 0:
                df['Class'][i] = 0

            change = re.sub(r"(</.*>)", "", df['Body'][i])
            change = re.sub(r"(<.*>)", "", change)

            stemmer = SnowballStemmer("english")
            splitted = re.split('\W+', change)
            singles = [stemmer.stem(word) for word in splitted]
            new_str = ""
            new_str += " ".join(singles)
            df['Body'][i] = new_str
            i = i + 1

        coef_test = 0.1
        X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['Body'], df['Class'], test_size=coef_test)

        test_size = int(np.math.ceil(coef_test * len(df)))
        X = np.array(df["Class"])
        X_lately = X[-test_size:]
        vectorizer = TfidfVectorizer()
        X_train = vectorizer.fit_transform(X_train_raw)
        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)
        X_test = vectorizer.transform(X_test_raw)
        predictions = classifier.predict(X_test)
        i = 0
        cnt_right = 0
        file = open(output_file, 'w')
        while i < len(predictions):
            file.write(str(predictions[i]))
            if predictions[i] == X_lately[i]:
                cnt_right = cnt_right + 1
            i = i+1

        right_predictions = cnt_right / len(predictions)
        print("Accuracy of predictions: " + str(right_predictions) + "%")

cf = clasificator()
clasificator.classify(cf, "./Answers.csv", "./classes.txt")
print("Done")

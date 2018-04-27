import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class text_with_score:
    text = ""
    score = 0
    def __init__(self, t, s):
        self.text = t
        self.score = s

df = pd.read_csv("./Answers.csv")
df.columns = ['Id', 'OwnerUserId', 'CreationDate', 'ParentId', 'Score', 'IsAcceptedAnswer', 'Body']
df['Class'] = np.sign(df['Score'])

X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['Body'], df['Class'],test_size=0.2)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

X_test = vectorizer.transform(X_test_raw)
predictions = classifier.predict(X_test)
print(predictions)
import quandl, math
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing, cross_validation

df = quandl.get('Wiki/GOOGL')
df.to_csv("GOOGL.csv")
df = df[['Open', 'High', 'Low', 'Close']]

forecast_col = 'Close'
forecast_out = int(math.ceil(0.01 * len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)

df = df.reset_index()
df = df[['Open', 'High', 'Low', 'Close', 'label']]

X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

df.dropna(inplace=True)
y = np.array(df['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)
print("R-squared: ")
print(model.score(X_test, y_test))

X = df[['Open']].values
y = df['Close'].values
model.fit(X, y)

plt.figure()
plt.xlabel('Open')
plt.ylabel('Close')
plt.plot(X, y, 'k.')

model.fit(X, y)
plt.plot(X, model.predict(X), color='g')
plt.show()
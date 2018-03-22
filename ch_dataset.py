import quandl
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_csv("./challenge_dataset.csv")
df.columns = ['x', 'y']
model = LinearRegression()
X = df[['x']].values
Y = df['y'].values
model.fit(X,Y)
plt.figure()
plt.xlabel('X')
plt.ylabel('Y')
plt.plot(X, Y, 'k.')
plt.plot(X, model.predict(X), color='g')

plt.grid(True)
plt.show()
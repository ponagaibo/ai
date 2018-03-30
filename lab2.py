import quandl
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = quandl.get('Wiki/GOOGL')
df.to_csv("GOOGL.csv")
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

df = df.reset_index()
df['Num'] = df.index
df = df[['Num', 'Open', 'High', 'Low', 'Close', 'Volume']]
print(df.head())

model = LinearRegression()
X = df[['Open']].values
y = df['Close'].values
model.fit(X, y)
plt.figure()
plt.xlabel('Open')
plt.ylabel('Close')
plt.plot(X, y, 'k.')
plt.plot(X, model.predict(X), color='g')

plt.grid(True)
plt.show()
import quandl
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math
import numpy as np

df = pd.read_csv("./global_co2.csv")
df.columns = ['Year', 'Total', 'Gas Fuel', 'Liquid Fuel', 'Solid Fuel', 'Cement', 'Gas Flaring', 'Per Capita']
per_cap = df['Per Capita'].values

i = 0
mx = 0.
# search first non nan value for mx
while i > len(per_cap):
    if not math.isnan(per_cap[i]):
        mx = per_cap[i]
        break
    i = i+1

i = 0
#search maximum value which is upper bound of array
while i < len(per_cap):
    if not math.isnan(per_cap[i]) and per_cap[i] > mx:
        mx = per_cap[i]
    i = i+1

i = 0
while i < len(per_cap):
    if math.isnan(per_cap[i]):
        per_cap[i] = mx * 2.
    i = i+1

# plot for outer value
X = df[['Year']].values
Y = per_cap
model = LinearRegression()
model.fit(X,Y)
plt.subplot(3, 1, 1)
plt.plot(X, Y, 'k.')
plt.plot(X, model.predict(X), color='g')
plt.title('Change NaN')
plt.ylabel('Out of bound')

# average instead nan
df = pd.read_csv("./global_co2.csv")
df.columns = ['Year', 'Total', 'Gas Fuel', 'Liquid Fuel', 'Solid Fuel', 'Cement', 'Gas Flaring', 'Per Capita']
per_cap = df['Per Capita'].values

i = 0
cnt = 0
sum = 0.
while i < len(per_cap):
    if not math.isnan(per_cap[i]):
        cnt = cnt + 1
        sum = sum + per_cap[i]
    i = i+1
av = sum / cnt

i = 0
while i < len(per_cap):
    if math.isnan(per_cap[i]):
        per_cap[i] = av
    i = i+1

Y = per_cap
model = LinearRegression()
model.fit(X,Y)
plt.subplot(3, 1, 2)
plt.plot(X, Y, 'k.')
plt.plot(X, model.predict(X), color='g')
plt.ylabel('Average')


# do not print if nan
df = pd.read_csv("./global_co2.csv")
df.columns = ['Year', 'Total', 'Gas Fuel', 'Liquid Fuel', 'Solid Fuel', 'Cement', 'Gas Flaring', 'Per Capita']
per_cap = df['Per Capita'].values

notnan = []
cnt = 0
i = 0
while i < len(per_cap):
    if not math.isnan(per_cap[i]):
        notnan[cnt:cnt] = [i]
        cnt = cnt + 1
    i = i+1

cnt = 0
newX = []
newY = []
for j in notnan:
    newX[cnt:cnt] = [X[j]]
    newY[cnt:cnt] = [per_cap[j]]
    cnt = cnt + 1

X = np.array(newX)
Y = newY
model = LinearRegression()
model.fit(X, Y)
plt.subplot(3, 1, 3)
plt.plot(X, Y, 'k.')
plt.plot(X, model.predict(X), color='g')
plt.xlabel('Year')
plt.ylabel('Without NaN')

plt.show()
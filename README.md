# ai
## Для файла "challenge_dataset.csv":

Построим линейную регрессию от двух имеющихся в файле столбцов:

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
    
![](https://sun1-5.userapi.com/c830608/v830608771/bb309/0qu3Gqc_uSg.jpg)


## Для файла "global_co2.csv":

В файле в столбце "Per Capita" содержатся значения NaN, поэтому нам нужно заменить
их на какие-нибудь числа. Например, построим три графика линейной регрессии 
"Per Capita" от "Year". В первом заменим NaN на значение, которое не входит в 
область значений столбца "Per Capita":

    df = pd.read_csv("./global_co2.csv")
    df.columns = ['Year', 'Total', 'Gas Fuel', 'Liquid Fuel', 'Solid Fuel', 
                  'Cement', 'Gas Flaring', 'Per Capita']
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

Во втором графике NaN заменено на среднее арифметическое значений столбца:

    df = pd.read_csv("./global_co2.csv")
    df.columns = ['Year', 'Total', 'Gas Fuel', 'Liquid Fuel', 'Solid Fuel', 
                  'Cement', 'Gas Flaring', 'Per Capita']
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
        
В третьем уберем все строки, в которых содержится NaN:

    df = pd.read_csv("./global_co2.csv")
    df.columns = ['Year', 'Total', 'Gas Fuel', 'Liquid Fuel', 'Solid Fuel', 
                  'Cement', 'Gas Flaring', 'Per Capita']
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
    
![Полученные графики](https://sun1-11.userapi.com/c840723/v840723498/6b3ac/vB5VaUEa05Y.jpg)

По графикам видно, что если заменить NaN на значение, которое не входит в нашу область
значений, это слишком сильно повлияет на прямую линейной регрессии и исказит
реальную зависимость. При замене NaN на среднее арифметическое возникает та же проблема. Лучше
всего линейная регрессия отображена на третьем графике, но для ее построения пришлось
пожертвовать слишком большим количеством данных. Если столбец "Per Capita" не очень
важен, то лучше удалить его, чем большую часть данных.

## Для файла "GOOGL.csv":

Построим линейную регрессию столбца 'Close' от столбца 'Open':
    plt.figure()
    plt.xlabel('Open')
    plt.ylabel('Close')
    plt.plot(X, y, 'k.')
    model.fit(X, y)
    plt.plot(X, model.predict(X), color='g')
    plt.show()

Интуитивно понятно, что их значения тесно связаны и один из столбцов может описывать другой. 
Полученный график:
![](https://sun9-9.userapi.com/c824701/v824701635/f431a/dy3J-elqKO4.jpg)
Теперь разделим данные на тренировочные и тестовые:

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("R-squared: ")
    print(model.score(X_test, y_test))

Значение "R-squared" показывает, насколько хорошо модель объясняет данные. В данном случае выдается значение 
около 0.85, что означает, что модель близка к переобучению.

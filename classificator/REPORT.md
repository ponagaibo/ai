# Отчет по лабораторной работе
## по курсу "Искусственый интеллект"

## Машинное обучение

### Студент: Понагайбо А.О.

## Результат проверки

| Преподаватель     | Дата         |  Оценка       |
|-------------------|--------------|---------------|
| Самир Ахмед |              |               |

> *Комментарии проверяющих (обратите внимание, что более подробные комментарии возможны непосредственно в репозитории по тексту программы)*

## Тема работы

Построить классификатор, выявляющий плохие ответы пользователя на языке Python (реализовать в виде класса). Подобрать или создать датасет и обучить модель. Продемонстрировать зависимость качества классификации от объема и качества выборки. Продемонстрировать работу вашего алгоритма. Обосновать выбор данного алгоритма машинного обучения.

## Решение
Для решения данной задачи была выбрана логистическая регрессия ввиду простоты ее применения. В качестве датасета была взята база ответов к вопросам по R со StackOverflow (https://www.kaggle.com/stackoverflow/rquestions). Датасет состоит из 250788 строк, в нем нет неотмеченных рейтингов, так что можно считать его хорошего качества.
Для каждого вопроса смотрим, если его рейтинг <= 0, то присваиваем ему класс 0 (плохой ответ), иначе - 1 (хороший ответ). Убираем из из тела ответа символы разметки, применяем к словам ответа стеммер Snawball, после чего тренируем модель. Для разных объемов тестовых выборок получились следующие точности:

| Процент тестовой выборки, %    | Точность, %        |
|--------------------------|--------------|
| 30 |   61%           |
|--------------------------|--------------|
| 20 |   60%           |
|--------------------------|--------------|
| 10 |   57%           |

Видно, что при большом проценте тренировочных данных классификация ухудшаются, что говорит о переобучении модели.

## Выводы

При выполнении данной лабораторной работы я познакомилась с логистической регрессией и стеммингом, построила зависимость классификации от объема данных
научилась строить линейную регрессию, различными способами обрабатывать 
недостающие данные (NaN), оценивать качество полученной модели. Также я познакомилась с инструментами в Python: 
quandl, pandas, sklearn, matplotlib, numpy.
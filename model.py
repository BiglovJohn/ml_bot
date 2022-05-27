import json
import re
import nltk
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

config_file = open("predictor_dataset.json", "r", encoding="utf-8")  # Открытие файла
BOT_CONFIG = json.load(config_file)  # Преобразование из JSON в структуру данных


def normalize(text):  # Создаем функцию, которая выкинет знаки препинания и приведет текст к нижнему регистру
    text = text.lower()  # "ПРиВЕт" => "привет"
    # Удалять из текста знаки препинания с помощью "Regular Expressions"
    punctuation = r"[^\w\s]"  # выражение позволяет удалить все знаки препинания
    # ^ - "все кроме"
    # \w - "буквы"
    # \s - "пробелы"

    # Старое выражение = \W = "все кроме букв"
    return re.sub(punctuation, "",
                  text)  # Заменяем все что попадает под шаблон punctuation на пустую строку "" в тексте text


def isMatching(text1, text2):  # Создаем функцию, которая посчитает похожи ли два текста
    text1 = normalize(text1)
    text2 = normalize(text2)
    distance = nltk.edit_distance(text1, text2)  # Посчитаем расстояние между текстами (насколько они отличается)
    average_length = (len(text1) + len(text2)) / 2  # Посчитаем среднюю длину текстов
    return distance / average_length < 0.4


def getIntent(text):  # Понимать намерение по тексту
    all_intents = BOT_CONFIG["intents"]
    for name, data in all_intents.items():  # Пройти по всем намерениям и положить название в name, и остальное в переменную data
        for example in data["examples"]:  # Пройти по всем примерам этого интента, и положить текст в переменную example
            if isMatching(text, example):  # Если текст совпадает с примером
                return name


def getAnswer(intent):
    responses = BOT_CONFIG["intents"][intent]["responses"]
    return random.choice(responses)


def bot(text):  # Функция = Бот
    # Пытаемся опеределить намерение
    intent = getIntent(text)

    if not intent:  # Если намерение не найдено
        test = vectorizer.transform([text])
        intent = model.predict(test)[0]  # По Х предсказать у, т.е. классифицировать

    print("Intent =", intent)

    if intent:  # Если намерение найдено - выдать ответ
        return getAnswer(intent)

    # Заглушка
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)


# тексты
x = []
# классы
y = []

# Задача модели по "x" научиться находить "y"
for name, data in BOT_CONFIG["intents"].items():
    for example in data["examples"]:
        x.append(example)  # Собираем тексты в "x"
        y.append(name)  # Собираем классы в "y"

vectorizer = CountVectorizer()  # В скобках можно указать настройки
vectorizer.fit(x)  # Передаём набор текстов, чтобы векторайзер их проанализировал
x_vectorized = vectorizer.transform(x)  # Трансформируем тексты в вектора (наборы чисел)

model = RandomForestClassifier()  # Настройки
model.fit(x_vectorized, y)  # Модель научится по "x" определять "y"

Countvect_RandomFor = model.score(x_vectorized, y)

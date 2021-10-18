from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import re


def getTokenize(text):
    tokens = word_tokenize(text)
    return tokens


def removeStopWords(text):
    readyText = []
    anySymbols = ["``", '``', "''"]
    stopword = stopwords.words('russian') + [a for a in punctuation] + anySymbols
    for word in text:
        if word not in stopword:
            readyText.append(word)
    return readyText


def deleteNumbers(text):
    textWithoutSymbols = []
    pattern = re.compile(r'[\d]+')
    for word in text:
        if not pattern.match(word):
            textWithoutSymbols.append(word)
    return textWithoutSymbols


def deleteSpaces(text):
    textWithoutSpaces = []
    pattern = re.compile(r'\s+')
    for word in text:
        if not pattern.match(word):
            textWithoutSpaces.append(word)
    return textWithoutSpaces


def deleteRepeatWords(text):
    setWords = set(text)
    return list(setWords)

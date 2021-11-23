from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import re
from natasha import NamesExtractor, MorphVocab
from nltk.stem.snowball import SnowballStemmer
import numpy as np
from lxml import etree
from sklearn.feature_extraction.text import CountVectorizer
from .apps import loadedClassif


def getTokenize(text):
    tokens = word_tokenize(text)
    return tokens


def removeStopWords(text):
    readyText = []
    anySymbols = ["``", '``', "''", "—", "."]
    anyWords = ["та", "иная", "риа", "апр", "на", "риа"]
    stopword = stopwords.words('russian') + [a for a in punctuation] + anySymbols + anyWords
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


def deleteNames(text):
    patternGetName = re.compile(r"(first='\S+')")
    listNames = []
    namesInFormat = []
    namesList = []
    textWithoutNames = []
    morph_vocab = MorphVocab()
    extractor = NamesExtractor(morph_vocab)
    for word in text:
        names = extractor.find(word)
        if names is not None:
            listNames.append(str(names))
    for name in listNames:
        stringNames = patternGetName.findall(name)
        if stringNames:
            namesInFormat.append(str(stringNames))
    for name in namesInFormat:
        namesList.append(name.split("'")[1])
    for word in text:
        if not word in namesList:
            textWithoutNames.append(word)
    return textWithoutNames


def getStem(text):
    stemTokens = []
    stemmer = SnowballStemmer("russian")
    for word in text:
        stemTokens.append(stemmer.stem(word))
    return stemTokens


def generateBow(text):
    pass


def tfVectorize(listText):
    # flatList = [item for sublist in listText for item in sublist]
    # print(flatList)
    # # listTf.append(stringTf)
    # # print(listTf)
    # vectorizer = TfidfVectorizer()
    # X = vectorizer.fit_transform(flatList)
    # # # print(len(vectorizer.get_feature_names_out()))
    # # xArray = X.toarray()
    # print(X)
    pass


def vectorize(text):
    lestRet = []
    textLoweCase = str(text).lower()
    tokenize = getTokenize(textLoweCase)
    tokenWithoutStop = removeStopWords(tokenize)
    tokenWithoutNumbers = deleteNumbers(tokenWithoutStop)
    tokenWithoutSpaces = deleteSpaces(tokenWithoutNumbers)
    deleteRepeatWord = deleteRepeatWords(tokenWithoutSpaces)
    deleteName = deleteNames(deleteRepeatWord)
    getSt = getStem(deleteName)
    string = " ".join(getSt)
    # vector = generateBow(getSt)
    # vector = tfVectorize(getSt)
    return string


def fillZerosVector(numpyArrays, listSize, attribute):
    fillsVectors = []
    maxSize = max(listSize)
    for array in numpyArrays:
        if np.size(array) != maxSize:
            while np.size(array) != maxSize:
                array = np.append(array, 0)
        array = np.append(array, attribute)
        fillsVectors.append(array)
    return fillsVectors


def saveReadyVectors(listOfVectors, sizeVector, attr, fileName):
    fillZeros = fillZerosVector(listOfVectors, sizeVector, attr)
    file = open(fileName, 'w')
    for fillVector in fillZeros:
        listVector = list(fillVector.astype("str"))
        StringVector = ",".join(listVector)
        file.write(StringVector + "\n")
    file.close()


def getPredictFile(nameFile):
    myDoc = etree.parse("xmlWEBApp/xml/" + str(nameFile) + ".xml")
    text = myDoc.find("./text").text
    vector = vectorize(text)
    Predict = loadedClassif.predict([vector])
    stringPredict = "Статья относится к классу - " + Predict
    return stringPredict


def getPredictText(text):
    vector = vectorize(text)
    Predict = loadedClassif.predict([vector])
    return Predict

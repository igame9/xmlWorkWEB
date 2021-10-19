from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import re
from natasha import NamesExtractor, MorphVocab
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer


def getTokenize(text):
    tokens = word_tokenize(text)
    return tokens


def removeStopWords(text):
    readyText = []
    anySymbols = ["``", '``', "''"]
    anyWords = ["та", "иная", "риа", "апр"]
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
    listBow = []
    stringBow = " ".join(text)
    listBow.append(stringBow)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(listBow)
    xArray = X.toarray()
    # print(xArray)
    # print(vectorizer.get_feature_names_out())
    return xArray


def vectorize(text):
    textLoweCase = str(text).lower()
    tokenize = getTokenize(textLoweCase)
    tokenWithoutStop = removeStopWords(tokenize)
    tokenWithoutNumbers = deleteNumbers(tokenWithoutStop)
    tokenWithoutSpaces = deleteSpaces(tokenWithoutNumbers)
    deleteRepeatWord = deleteRepeatWords(tokenWithoutSpaces)
    deleteName = deleteNames(deleteRepeatWord)
    getSt = getStem(deleteName)
    vectorize = generateBow(getSt)
    return vectorize

import os
from django.http import HttpResponse
from lxml import etree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from . import functionsNLP
from sklearn.svm import SVC  # метод опорных векторов
import numpy as np
import shutil
import pickle
from .apps import loadedClassif


#  Другие методы МL, еще больше - в библиотеке.
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.svm import SVC

# for root, dirs, files in os.walk("xmlWEBApp/xml"):
#     for filename in files:


def nlp(request):
    if request.method == "GET":
        listPolitic = []
        listIncident = []
        listCulture = []

        for root, dirs, files in os.walk("XMLculture"):
            for filename in files:
                listCulture.append(filename)

        for root, dirs, files in os.walk("XMLincident"):
            for filename in files:
                listIncident.append(filename)

        for root, dirs, files in os.walk("XMLpolitics"):
            for filename in files:
                listPolitic.append(filename)
        #
        # listVectors = []
        # sizeVector = []
        # generalList = listPolitic + listIncident + listCulture
        #
        # for gen in generalList:  # макисмальная длина вектора из всех
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(gen))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     sizeVector.append(np.size(numpyArray))
        #
        # for pol in listPolitic:
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(pol))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     listVectors.append(numpyArray)
        #     functionsNLP.saveReadyVectors(listVectors, sizeVector, 1, "politics.txt")
        # listVectors.clear()
        #
        # for incident in listIncident:
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(incident))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     listVectors.append(numpyArray)
        #     functionsNLP.saveReadyVectors(listVectors, sizeVector, 2, "incidents.txt")
        # listVectors.clear()
        #
        # for culture in listCulture:
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(culture))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     listVectors.append(numpyArray)
        #     functionsNLP.saveReadyVectors(listVectors, sizeVector, 3, "culture.txt")
        # listVectors.clear()

        with open('readyCoords.txt', 'wb') as outFile:
            for file in ['politics.txt', 'incidents.txt', 'culture.txt']:
                with open(file, 'rb') as file:
                    shutil.copyfileobj(file, outFile)

        return HttpResponse("Составление векторов признаков")


def learnModel(request):
    if request.method == "GET":
        rawData = open("readyCoords.txt")
        dataset = np.loadtxt(rawData, delimiter=",")
        svmClassifier = SVC()
        svmClassifier.fit(dataset[:, :-1], dataset[:, -1])
        pickle.dump(svmClassifier, open("modelSVM.dat", 'wb'))
        return HttpResponse("Обучение")


def testLearn(request):
    if request.method == "GET":
        listSize = [864]
        listVectors = []

        myDoc = etree.parse("xmlWEBApp/xml/" + "Уголовное дело возбудили в селе Верхневилюйск.xml")
        text = myDoc.find("./text").text
        vector = functionsNLP.vectorize(text)
        numpyArray = np.array(vector)
        listVectors.append(numpyArray)
        readyVector = functionsNLP.fillZerosVector(listVectors, listSize, 0)
        Predict = loadedClassif.predict(readyVector)
        # accuracy = accuracy_score(Predict, Predict) результа и какие должны быть
        # print(accuracy)
        return HttpResponse(Predict)

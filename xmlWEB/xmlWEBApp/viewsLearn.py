import os
import pickle

from django.http import HttpResponse
from lxml import etree
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.pipeline import Pipeline

from . import functionsNLP
import numpy as np

from .apps import loadedClassif


# for root, dirs, files in os.walk("xmlWEBApp/xml"):
#     for filename in files:


def nlp(request):
    if request.method == "GET":
        # listPolitic = []
        # listIncident = []
        listCulture = ["firstThreadculture0", "firstThreadculture1", "firstThreadculture2", "firstThreadculture3",
                       "firstThreadculture4", "firstThreadculture5"]
        # listWithoutTfIdf = []

        # for root, dirs, files in os.walk("XMLculture"):
        #     for filename in files:
        #         listCulture.append(filename)
        #
        # for root, dirs, files in os.walk("XMLincidents"):
        #     for filename in files:
        #         listIncident.append(filename)
        #
        # for root, dirs, files in os.walk("XMLpolitics"):
        #     for filename in files:
        #         listPolitic.append(filename)

        # listVectors = []
        # sizeVector = []
        # generalList = listPolitic + listIncident + listCulture
        #
        # i = 0
        # for gen in generalList:  # макисмальная длина вектора из всех
        #     print(gen)
        #     i = i + 1
        #     print(i)
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(gen))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     sizeVector.append(np.size(numpyArray))
        # print("Общая размерность установлена")
        # i = 0
        # for pol in listPolitic:
        #     print(pol)
        #     i = i + 1
        #     print(i)
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(pol))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     listVectors.append(numpyArray)
        #     functionsNLP.saveReadyVectors(listVectors, sizeVector, 1, "politics.txt")
        # listVectors.clear()

        # i = 0
        # for incident in listIncident:
        #     print(incident)
        #     i = i + 1
        #     print(i)
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(incident))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     listVectors.append(numpyArray)
        #     functionsNLP.saveReadyVectors(listVectors, sizeVector, 2, "incidents.txt")
        # listVectors.clear()
        #
        # i = 0
        # for culture in listCulture:
        #     print(culture)
        #     i = i + 1
        #     print(i)
        #     myDoc = etree.parse("xmlWEBApp/xml/" + str(culture))
        #     text = myDoc.find("./text").text
        #     vector = functionsNLP.vectorize(text)
        #     numpyArray = np.array(vector)
        #     listVectors.append(numpyArray)
        #     functionsNLP.saveReadyVectors(listVectors, sizeVector, 3, "culture.txt")
        # listVectors.clear()
        #
        # with open('readyCoords.txt', 'wb') as outFile:
        #     for file in ['politics.txt', 'incidents.txt', 'culture.txt']:
        #         with open(file, 'rb') as file:
        #             shutil.copyfileobj(file, outFile)
        #
        listStr = []
        i = 0
        for root, dirs, files in os.walk("xmlWEBApp/xml"):
            for filename in files:
                myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                text = myDoc.find("./text").text
                category = myDoc.find("./category").text
                vect = functionsNLP.vectorize(text)  # тут вид самих статей
                listStr.append([vect, category])
                i = i + 1
                print(i)

        dataFrame = pd.DataFrame(listStr, columns=("Text", "class"))
        print(dataFrame)
        dataFrame.to_csv('dataFrame.csv', index=False)
        return HttpResponse("Составление векторов признаков")


def learnModel(request):
    if request.method == "GET":
        # rawData = open("readyCoords.txt")
        # dataset = np.loadtxt(rawData, delimiter=",")
        # svmClassifier = SVC()
        # clf = LogisticRegression(random_state=0)
        # kernel = 1.0 * RBF(1.0)
        # gpc = GaussianProcessClassifier(kernel=kernel, random_state=0)
        # clf = GaussianNB()
        # KNNmodel = KNeighborsClassifier(n_neighbors=1)
        # clf = LogisticRegression(random_state=0)
        # clf.fit(dataset[:, :-1], dataset[:, -1])
        # regressor = RandomForestRegressor(n_estimators=20, random_state=0)
        # clf = LinearDiscriminantAnalysis()
        # clf = MLPClassifier(random_state=1, max_iter=300)
        # KNNmodel.fit(dataset[:, :-1], dataset[:, -1])
        # pickle.dump(KNNmodel, open("test.dat", 'wb'))

        dataSet = pd.read_csv("dataFrame.csv")
        X = dataSet['Text']
        y = dataSet['class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=15)

        KNN = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', KNeighborsClassifier(n_neighbors=1))])
        KNN.fit(X_train, y_train)
        pickle.dump(KNN, open("KNN.dat", 'wb'))
        return HttpResponse("Обучение")


def testLearn(request):
    if request.method == "GET":

        myDoc = etree.parse("xmlWEBApp/xml/" + "Тест МЛ.xml")
        text = myDoc.find("./text").text
        vector = functionsNLP.vectorize(text)

        Predict = loadedClassif.predict([vector])
        # accuracy = accuracy_score(Predict, Predict) результа и какие должны быть
        # print(accuracy)
        return HttpResponse(Predict)


def accuracyClassif(request):
    if request.method == "GET":
        dataSet = pd.read_csv("dataFrame.csv")
        X = dataSet['Text']
        y = dataSet['class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)
        predict = loadedClassif.predict(X_test)
        # print(classification_report(KNNPredict, y_test))
        return HttpResponse(accuracy_score(predict, y_test))

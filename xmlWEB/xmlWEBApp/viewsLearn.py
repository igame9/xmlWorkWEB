from django.http import HttpResponse
from lxml import etree
from . import functionsNLP
from sklearn.svm import SVC  # метод опорных векторов
import numpy as np
import shutil
import pickle


#  Другие методы МL, еще больше - в библиотеке.
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.svm import SVC

def nlp(request):
    if request.method == "GET":
        # for root, dirs, files in os.walk("xmlWEBApp/xml"):
        #     for filename in files:
        listPolitic = ["firstThread132.xml", "firstThread148.xml", "firstThread139.xml"]
        listMedicine = ["firstThread133.xml", "firstThread149.xml", "firstThread165.xml", "firstThread189.xml"]
        listCatastrophe = ["firstThread14.xml", "firstThread159.xml", "firstThread27.xml"]
        listVectors = []
        sizeVector = []
        generalList = listPolitic + listMedicine + listCatastrophe

        for gen in generalList:  # макисмальная длина вектора из всех
            myDoc = etree.parse("xmlWEBApp/xml/" + str(gen))
            text = myDoc.find("./text").text
            vector = functionsNLP.vectorize(text)
            numpyArray = np.array(vector)
            sizeVector.append(np.size(numpyArray))

        for pol in listPolitic:
            myDoc = etree.parse("xmlWEBApp/xml/" + str(pol))
            text = myDoc.find("./text").text
            vector = functionsNLP.vectorize(text)
            numpyArray = np.array(vector)
            listVectors.append(numpyArray)
            functionsNLP.saveReadyVectors(listVectors, sizeVector, 1, "politics.txt")
        listVectors.clear()

        for medicine in listMedicine:
            myDoc = etree.parse("xmlWEBApp/xml/" + str(medicine))
            text = myDoc.find("./text").text
            vector = functionsNLP.vectorize(text)
            numpyArray = np.array(vector)
            listVectors.append(numpyArray)
            functionsNLP.saveReadyVectors(listVectors, sizeVector, 2, "medicine.txt")
        listVectors.clear()

        for catastrophe in listCatastrophe:
            myDoc = etree.parse("xmlWEBApp/xml/" + str(catastrophe))
            text = myDoc.find("./text").text
            vector = functionsNLP.vectorize(text)
            numpyArray = np.array(vector)
            listVectors.append(numpyArray)
            functionsNLP.saveReadyVectors(listVectors, sizeVector, 3, "catastrophe.txt")
        listVectors.clear()

        with open('readyCoords.txt', 'wb') as outFile:
            for file in ['politics.txt', 'medicine.txt', 'catastrophe.txt']:
                with open(file, 'rb') as file:
                    shutil.copyfileobj(file, outFile)

    return HttpResponse("Составление векторов признаков")


def learnModel(request):
    if request.method == "GET":
        rawData = open("readyCoords.txt")
        dataset = np.loadtxt(rawData, delimiter=",")
        svmClassifier = SVC()
        svmClassifier.fit(dataset[:, :-1], dataset[:, -1])
        pickle.dump(svmClassifier, open("model.dat", 'wb'))
        return HttpResponse("Обучение")

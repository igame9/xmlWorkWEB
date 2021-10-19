from django.http import HttpResponse
from lxml import etree
from . import functionsNLP
from sklearn.svm import SVC


def nlp(request):
    if request.method == "GET":
        # for root, dirs, files in os.walk("xmlWEBApp/xml"):
        #     for filename in files:
        listPolitic = ["firstThread132.xml", "firstThread148.xml", "firstThread139.xml"]
        listMedicine = ["firstThread133.xml", "firstThread149.xml", "firstThread165.xml", "firstThread189.xml"]
        listCatastrophe = ["firstThread14.xml", "firstThread159.xml", "firstThread27.xml"]
        for pol in listPolitic:
            myDoc = etree.parse("xmlWEBApp/xml/" + str(pol))
            text = myDoc.find("./text").text
            vector = functionsNLP.vectorize(text)
            print(vector)

    return HttpResponse("Обучение")

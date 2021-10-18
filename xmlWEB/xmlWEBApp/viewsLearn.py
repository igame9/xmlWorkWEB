from django.http import HttpResponse
from lxml import etree
from . import functionsNLP


def nlp(request):
    if request.method == "GET":
        # for root, dirs, files in os.walk("xmlWEBApp/xml"):
        #     for filename in files:
        myDoc = etree.parse("xmlWEBApp/xml/" + "firstThread4.xml")
        text = myDoc.find("./text").text
        textLoweCase = str(text).lower()
        tokenize = functionsNLP.getTokenize(textLoweCase)
        tokenWithoutStop = functionsNLP.removeStopWords(tokenize)
        tokenWithoutNumbers = functionsNLP.deleteNumbers(tokenWithoutStop)
        tokenWithoutSpaces = functionsNLP.deleteSpaces(tokenWithoutNumbers)
        deleteRepeatWords = functionsNLP.deleteRepeatWords(tokenWithoutSpaces)
        deleteNames = functionsNLP.deleteNames(deleteRepeatWords)
        getStem = functionsNLP.getStem(deleteNames)
        print(getStem)
    return HttpResponse("Обучение")

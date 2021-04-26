from django.shortcuts import render
from django.http import HttpResponse
import os
import xml.etree.ElementTree as Etree


# Create your views here.
def index(request):
    listWithXml = []
    for root, dirs, files in os.walk("xmlWEBApp/xml"):
        for filename in files:
            listWithXml.append(filename)
    return render(request, "index.html", {"xmlList": listWithXml})


def xml(request, any):
    # file = open("xmlWEBApp/xml/" + str(any) + ".xml", "r", encoding="utf-8")

    myDoc = Etree.parse("xmlWEBApp/xml/" + str(any) + ".xml")
    category = myDoc.find("./category").text
    title = myDoc.find("./title").text
    dateAndTime = myDoc.find("./DateAndTime").text
    views = myDoc.find("./views").text
    text = myDoc.find("./text").text
    tags = myDoc.find("./tags").text

    # textXml = file.read()
    return render(request, "xmlPlace.html",
                  {"nameXml": any,
                   "category": category,
                   "title": title,
                   "dateAndTime": dateAndTime,
                   "views": views,
                   "text": text,
                   "tags": tags})


def saveChange(request):
    if request.method == "post":
        return HttpResponse("б")
    return HttpResponse("а")

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
    file = open("xmlWEBApp/xml/" + str(any) + ".xml", "r", encoding="utf-8")
    # for line in file:
    #     textXml.append(line)
    textXml = file.read()
    return render(request, "xmlPlace.html", {"nameXml": any, "textXml": textXml})

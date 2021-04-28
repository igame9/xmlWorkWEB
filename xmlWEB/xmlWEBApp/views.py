from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import os
import xml.etree.ElementTree as Etree
# from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.core.exceptions import SuspiciousOperation


def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }


# Create your views here.
def index(request):
    listWithXml = []
    for root, dirs, files in os.walk("xmlWEBApp/xml"):
        for filename in files:
            listWithXml.append(filename)
    paginator = Paginator(listWithXml, 10)
    page = request.GET.get('page')
    try:
        xmlPag = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        xmlPag = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        xmlPag = paginator.page(paginator.num_pages)
    return render(request, "index.html", {"xmlPag": xmlPag})


def xml(request, any):
    # file = open("xmlWEBApp/xml/" + str(any) + ".xml", "r", encoding="utf-8")
    try:
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
    except FileNotFoundError:
        return HttpResponseRedirect(reverse('xmlWEBApp:_indexPage_'))


def saveChange(request):
    if request.method == 'POST' and request.is_ajax():
        data = request.body.decode('utf-8')
        jsonData = json.loads(data)
        changeCategory = jsonData["category"]
        changeTitle = jsonData["title"]
        changeDateAndTime = jsonData["dateAndTime"]
        changeViews = jsonData["views"]
        changeText = jsonData["text"]
        changeTag = jsonData["tags"]
        nameFile = jsonData["nameFile"]
        myDoc = Etree.parse("xmlWEBApp/xml/" + str(nameFile) + ".xml")
        myDoc.find("./category").text = changeCategory
        myDoc.find("./title").text = changeTitle
        myDoc.find("./DateAndTime").text = changeDateAndTime
        myDoc.find("./views").text = changeViews
        myDoc.find("./text").text = changeText
        myDoc.find("./tags").text = changeTag
        # pathToRedirect = "/" + str(nameFile) + ".xml" + "/"
        myDoc.write("xmlWEBApp/xml/" + str(nameFile) + ".xml", encoding="utf-8")
        messages.success(request, 'Изменения сохранены')
        return HttpResponse(200)


def deleteFile(request):
    if request.method == 'DELETE' and request.is_ajax():
        data = request.body.decode('utf-8')
        jsonData = json.loads(data)
        nameFile = jsonData["nameFile"]
        print(nameFile)
        path = os.path.join("./xmlWEBApp/xml/", str(nameFile) + ".xml")
        os.remove(path)
        return HttpResponse(200)


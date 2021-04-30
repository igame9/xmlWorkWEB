import json
import os

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
import re


def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }


# Create your views here.
@csrf_exempt
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


@csrf_exempt
def xml(request, any):
    # file = open("xmlWEBApp/xml/" + str(any) + ".xml", "r", encoding="utf-8")
    try:
        myDoc = etree.parse("xmlWEBApp/xml/" + str(any) + ".xml")
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
    except (FileNotFoundError, OSError):
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
        myDoc = etree.parse("xmlWEBApp/xml/" + str(nameFile) + ".xml")
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
        path = os.path.join("./xmlWEBApp/xml/", str(nameFile) + ".xml")
        os.remove(path)
        return HttpResponse(200)


def newXML(request):
    if request.method == 'POST' and request.is_ajax():
        data = request.body.decode('utf-8')
        jsonData = json.loads(data)
        nameFile = jsonData["nameFile"]
        category = jsonData["category"]
        title = jsonData["title"]
        dateTime = jsonData["dateAndTime"]
        view = jsonData["views"]
        text = jsonData["text"]
        tags = jsonData["tags"]
        if nameFile == "" or category == "" or title == "" or dateTime == "" \
                or view == "" or text == "" or tags == "":
            # messages.warning(request, "Требуется заполнить все данные")
            return HttpResponse(json.dumps("Необходимо  заполнить все данные"))
        else:
            xmlData = etree.Element("doc")
            # sourceXmlData = etree.SubElement(xmlData, "source")
            # sourceXmlData.text = etree.CDATA(driver.current_url) ; запись источника данных

            categoryXmlData = etree.SubElement(xmlData, "category")
            categoryXmlData.attrib['verify'] = "true"
            categoryXmlData.attrib['type'] = "str"
            categoryXmlData.attrib['auto'] = "true"

            titleXmlData = etree.SubElement(xmlData, "title")
            titleXmlData.attrib['verify'] = "true"
            titleXmlData.attrib['type'] = "str"
            titleXmlData.attrib['auto'] = "true"

            dateAndTime = etree.SubElement(xmlData, "DateAndTime")
            dateAndTime.attrib['verify'] = "true"
            dateAndTime.attrib['type'] = "str"
            dateAndTime.attrib['auto'] = "true"

            views = etree.SubElement(xmlData, "views")
            views.attrib['verify'] = "true"
            views.attrib['type'] = "str"
            views.attrib['auto'] = "true"

            textXmlData = etree.SubElement(xmlData, "text")
            textXmlData.attrib['verify'] = "true"
            textXmlData.attrib['type'] = "str"
            textXmlData.attrib['auto'] = "true"

            tagsXmlData = etree.SubElement(xmlData, "tags")
            tagsXmlData.attrib['verify'] = "true"
            tagsXmlData.attrib['type'] = "str"
            tagsXmlData.attrib['auto'] = "true"

            categoryXmlData.text = category
            titleXmlData.text = str(title)
            dateAndTime.text = str(dateTime)
            views.text = str(view)
            textXmlData.text = str(text)
            tagsXmlData.text = str(tags)
            nameFileXML = str(nameFile)

            xmlTree = etree.ElementTree(xmlData)
            xmlTree.write(r"./xmlWEBApp/xml/" + str(nameFileXML) + ".xml", encoding="utf-8", xml_declaration=True,
                          pretty_print=True)
            return HttpResponse(json.dumps("Статья успешно создана"))

    if request.method == 'GET':
        return render(request, "newXML.html")


def findXML(request):
    listSearchFiles = []
    data = request.POST.get("reg")
    examplePattern = re.compile("(" + str(data) + ".+)")  # ("(.*" + "[" + str(data) + "]" + "+.*)")
    for root, dirs, files in os.walk("xmlWEBApp/xml"):
        for filename in files:
            if examplePattern.fullmatch(filename):
                listSearchFiles.append(str(filename))

    if request.method == 'POST':
        paginator = Paginator(listSearchFiles, 15)
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

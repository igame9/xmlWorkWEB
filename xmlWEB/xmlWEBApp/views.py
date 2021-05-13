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
from datetime import date


def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }


# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "GET":
        listWithXml = []
        categoryList = []
        patternWords = re.compile("([А-Яа-я]+)")
        for root, dirs, files in os.walk("xmlWEBApp/xml"):
            for filename in files:
                myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                categoryArticles = myDoc.find("./category").text
                categoryList.append(categoryArticles)
                listWithXml.append(filename)
        # print(",".join(tagsList))
        stringTags = ",".join(categoryList)
        patternWords = re.compile("([А-Яа-я]+)")
        readyTags = set(patternWords.findall(stringTags))

        paginator = Paginator(listWithXml, 15)
        page = request.GET.get('page')
        try:
            xmlPag = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            xmlPag = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            xmlPag = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"xmlPag": xmlPag,
                                              "readyTags": readyTags})


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
    if request.method == 'POST':
        listSearchFiles = []
        data = request.POST.get("reg")  # nameFile

        startDate = request.POST.get("firstDate")
        endDate = request.POST.get("secondDate")
        tags = request.POST.get("tags")

        if tags != "":
            for root, dirs, files in os.walk("xmlWEBApp/xml"):
                for filename in files:
                    myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                    patternWords = re.compile("([А-Яа-я]+)")
                    enteredTags = patternWords.findall(tags)
                    tagsArticles = myDoc.find("./tags").text
                    tagsForCompare = patternWords.findall(tagsArticles)
                    for tag in enteredTags:
                        for cmpTag in tagsForCompare:
                            if tag == cmpTag:
                                # print("Равно")
                                listSearchFiles.append(str(filename))

        if data != "":
            examplePattern = re.compile("(" + str(data) + ".+)")  # ("(.*" + "[" + str(data) + "]" + "+.*)")
            for root, dirs, files in os.walk("xmlWEBApp/xml"):
                for filename in files:
                    if examplePattern.match(filename):
                        listSearchFiles.append(str(filename))
        else:
            pass

        if startDate != "" or endDate != "":
            if endDate == "":
                endDate = startDate
            if startDate == "":
                startDate = endDate

            datePattern = re.compile(r"(\d*\.\d*\.\d*)")
            yearStart, mothStart, dayStart = str(startDate).split("-")
            convertedStartDate = date(int(yearStart), int(mothStart), int(dayStart))
            yearEnd, mothEnd, dayEnd = str(endDate).split("-")
            convertedEndDate = date(int(yearEnd), int(mothEnd), int(dayEnd))
            for root, dirs, files in os.walk("xmlWEBApp/xml"):
                for filename in files:
                    myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                    dateAndTime = myDoc.find("./DateAndTime").text
                    onlyDate = datePattern.findall(dateAndTime)

                    if onlyDate:
                        day, month, year = str(onlyDate).replace("[", "").replace("]", "").replace("'", "").split(".")
                        dateToDate = date(int(year), int(month), int(day))
                        if convertedStartDate <= dateToDate <= convertedEndDate:
                            listSearchFiles.append(str(filename))
        else:
            pass

        listSearchFiles = list(set(listSearchFiles))
        request.session['data'] = listSearchFiles
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

    if request.method == "GET":
        paginator = Paginator(request.session['data'], 15)
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

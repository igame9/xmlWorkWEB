import json
import os

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from lxml import etree
from datetime import date
from . import functions
from . import functionsNLP


# Create your views here.
@csrf_exempt
def index(request):  # заполнение индексной страницы
    if request.method == "GET":
        listWithXml = {}
        categoryList = []
        paginatorDict = tuple()
        for root, dirs, files in os.walk("xmlWEBApp/xml"):
            for filename in files:
                myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                categoryArticles = myDoc.find("./category").text
                title = myDoc.find("./title").text
                categoryList.append(categoryArticles)
                listWithXml.setdefault(str(filename).rstrip(".xml"), title)  # print(",".join(tagsList))
                paginatorDict = tuple(listWithXml.items())

        readyTags = functions.getCategory()

        paginator = Paginator(paginatorDict, 15)
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
def xml(request, any):  # any - name of file, открытие xml файла
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
    except (FileNotFoundError, OSError):  # несуществующий файл и его чтение
        return HttpResponseRedirect(reverse('xmlWEBApp:_indexPage_'))


@csrf_protect
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


@csrf_protect
def deleteFile(request):
    if request.method == 'DELETE' and request.is_ajax():
        data = request.body.decode('utf-8')
        jsonData = json.loads(data)
        nameFile = jsonData["nameFile"]
        path = os.path.join("./xmlWEBApp/xml/", str(nameFile) + ".xml")
        os.remove(path)
        return HttpResponse(200)


@csrf_protect
def newXML(request):
    if request.method == 'POST' and request.is_ajax():
        data = request.body.decode('utf-8')
        jsonData = json.loads(data)
        nameFile = jsonData["nameFile"]
        category = jsonData["category"]
        title = jsonData["title"]
        dateTime = jsonData["dateAndTime"]
        text = jsonData["text"]
        tags = jsonData["tags"]
        correct = 0

        if nameFile == "" or category == "" or title == "" or dateTime == "" \
                or text == "" or tags == "":
            # messages.warning(request, "Требуется заполнить все данные")
            return HttpResponse(json.dumps("Необходимо  заполнить все данные"))
        else:
            correct = correct + 1

        try:
            day, month, year = str(dateTime).replace("[", "").replace("]", "").replace("'", "").split(".")
            checkDate = date(int(year), int(month), int(day))
        except ValueError:
            return HttpResponse(json.dumps("Некорректная дата"))
        else:
            correct = correct + 1

        if correct == 2:
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
            views.text = str("Статья создана вручную")
            textXmlData.text = str(text)
            tagsXmlData.text = str(tags)
            nameFileXML = str(nameFile)

            xmlTree = etree.ElementTree(xmlData)
            xmlTree.write(r"./xmlWEBApp/xml/" + str(nameFileXML) + ".xml", encoding="utf-8", xml_declaration=True,
                          pretty_print=True)
            return HttpResponse(json.dumps("Статья успешно создана"))

    if request.method == 'GET':
        return render(request, "newXML.html")


@csrf_protect
def findXML(request):
    if request.method == 'POST':

        data = request.POST.get("reg")  # nameFile
        startDate = request.POST.get("firstDate")
        endDate = request.POST.get("secondDate")
        tags = request.POST.get("tags")
        category = request.POST.get("category")

        sortValue = request.POST.get("sort")
        request.session['findNameFile'] = ""
        request.session['findStartDate'] = ""
        request.session['findEndDate'] = ""
        request.session['findTags'] = ""
        request.session['findCategory'] = ""
        request.session['findSort'] = ""

        if data != "":
            request.session['findNameFile'] = str(data)
        if startDate != "":
            request.session['findStartDate'] = str(startDate)
        if endDate != "":
            request.session['findEndDate'] = str(endDate)
        if tags != "":
            request.session['findTags'] = str(tags)
        if category != "":
            request.session['findCategory'] = str(category)

        if sortValue == "nameSort":
            request.session['findSort'] = "nameSort"
            sortName = True
        else:
            sortName = False

        if sortValue == "dateSort":
            request.session['findSort'] = "dateSort"
            dateSort = True
        else:
            dateSort = False

        if sortValue == "viewSort":
            request.session['findSort'] = "viewSort"
            viewSort = True
        else:
            viewSort = False

        listSearchFiles = functions.getListSearchFiles(category, tags, data, startDate, endDate)
        listAnd = functions.getListAnd(listSearchFiles, startDate, endDate, data, category, tags)
        request.session['data'] = listAnd  # на случай, если не было сортировки, чтобы сессионная переменная не была
        # пустой Записываю либо после сортировки, либо при окночательном заполнении listAnd
        functions.makeSort(sortName, dateSort, listAnd, viewSort, request)

        request.session['tagsReady'] = functions.getCategory()  # Список категорий

        paginatorDict = tuple(request.session['data'].items())
        paginator = Paginator(paginatorDict, 15)
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
                                              "readyTags": request.session['tagsReady'],
                                              "findNameFile": request.session['findNameFile'],
                                              "findStartDate": request.session['findStartDate'],
                                              "findEndDate": request.session['findEndDate'],
                                              "findTags": request.session['findTags'],
                                              "findCategory": request.session['findCategory'],
                                              "findSort": request.session['findSort']
                                              })

    if request.method == "GET":
        paginatorDict = tuple(request.session['data'].items())
        paginator = Paginator(paginatorDict, 15)
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
                                              "readyTags": request.session['tagsReady'],
                                              "findNameFile": request.session['findNameFile'],
                                              "findStartDate": request.session['findStartDate'],
                                              "findEndDate": request.session['findEndDate'],
                                              "findTags": request.session['findTags'],
                                              "findCategory": request.session['findCategory'],
                                              "findSort": request.session['findSort']
                                              })


def getPredict(request):
    if request.method == 'POST' and request.is_ajax():
        data = request.body.decode('utf-8')
        jsonData = json.loads(data)
        nameFile = jsonData["nameFile"]
        predict = functionsNLP.getPredictFile(nameFile)
        return HttpResponse(predict)


def autoFillArticle(request):
    if request.method == 'POST' and request.is_ajax():
        dictWithFillData = {}
        data = request.body.decode('utf-8')
        jsonData = json.loads(data)
        text = jsonData["text"]
        if text == "":
            return HttpResponse(json.dumps("Text Not Found"))
        classOfArticle = functionsNLP.getPredictText(text)
        dictWithFillData.setdefault("category", str(classOfArticle).replace("'", "").replace("[", "").replace("]", ""))
        bagOfWords = functionsNLP.generateBow(text)
        print(bagOfWords)
        return JsonResponse(json.loads(json.dumps(dictWithFillData)))

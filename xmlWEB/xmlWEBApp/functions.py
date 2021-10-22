# Функции для работы с views
import os
import re
from datetime import date

from lxml import etree


def getListSearchFiles(category, tags, data, startDate, endDate):
    listSearchFiles = {}
    if category != "":
        for root, dirs, files in os.walk("xmlWEBApp/xml"):
            for filename in files:
                myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                categoryInFile = myDoc.find("./category").text
                title = myDoc.find("./title").text
                if str(categoryInFile) == str(category):
                    listSearchFiles.setdefault(str(filename.rstrip(".xml")), title)
                    # print(listSearchFiles)

    else:
        pass

    if tags != "":
        for root, dirs, files in os.walk("xmlWEBApp/xml"):
            for filename in files:
                myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                patternWords = re.compile("([А-Яа-я]+)")  # ([а-яА-Я0-9_ ]+)  ([А-Яа-я]+)
                enteredTags = patternWords.findall(tags)
                tagsArticles = myDoc.find("./tags").text
                title = myDoc.find("./title").text
                tagsForCompare = patternWords.findall(tagsArticles)
                for tag in enteredTags:
                    for cmpTag in tagsForCompare:
                        if tag == cmpTag:
                            # print("Равно")
                            listSearchFiles.setdefault(str(filename.rstrip(".xml")), title)

    if data != "":
        examplePattern = re.compile("(" + str(data) + ".+" + ")")
        # ("(.*" + "[" + str(data) + "]" + "+.*)")
        # #("(" + str(data) + ".+)")
        for root, dirs, files in os.walk("xmlWEBApp/xml"):
            for filename in files:
                myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
                title = myDoc.find("./title").text
                if examplePattern.match(title):
                    # print(title)
                    listSearchFiles.setdefault(str(filename.rstrip(".xml")), title)
                    # print(listSearchFiles)

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
                title = myDoc.find("./title").text
                onlyDate = datePattern.findall(dateAndTime)

                if onlyDate:
                    day, month, year = str(onlyDate).replace("[", "").replace("]", "").replace("'", "").split(".")
                    dateToDate = date(int(year), int(month), int(day))
                    if convertedStartDate <= dateToDate <= convertedEndDate:
                        listSearchFiles.setdefault(str(filename.rstrip(".xml")), title)

    else:
        pass

    # listSearchFiles = list(set(listSearchFiles))
    return listSearchFiles


def getListAnd(listSearchFiles, startDate, endDate, data, category, tags):
    listAnd = {}
    for key, value in listSearchFiles.items():  # and instead or
        # print(key)
        # print(value)
        countNot = 0
        myDoc = etree.parse("xmlWEBApp/xml/" + str(key) + ".xml")
        # find date
        if startDate != "" or endDate != "":
            if endDate == "":
                endDate = startDate
            if startDate == "":
                startDate = endDate
            yearStart, mothStart, dayStart = str(startDate).split("-")
            convertedStartDate = date(int(yearStart), int(mothStart), int(dayStart))
            yearEnd, mothEnd, dayEnd = str(endDate).split("-")
            convertedEndDate = date(int(yearEnd), int(mothEnd), int(dayEnd))

            datePattern = re.compile(r"(\d*\.\d*\.\d*)")
            dateAndTime = myDoc.find("./DateAndTime").text
            onlyDate = datePattern.findall(dateAndTime)
            if onlyDate:
                day, month, year = str(onlyDate).replace("[", "").replace("]", "").replace("'", "").split(".")
                dateToDate = date(int(year), int(month), int(day))
                if not (convertedStartDate <= dateToDate <= convertedEndDate):
                    countNot = countNot + 1

        else:
            pass
        # ......
        # find name
        examplePattern = re.compile("(" + str(data) + ".+" + ")")
        if not examplePattern.match(value):  # здесь сравнивал по имени файла вместо заголовка!!!
            countNot = countNot + 1

        # ........
        # find tags
        # listEq = []
        countHaveTag = 0  # теги, которые есть в файле и были введены
        countNoTag = 0
        patternWords = re.compile("([А-Яа-я]+)")
        enteredTags = patternWords.findall(tags)
        tagsArticles = myDoc.find("./tags").text
        tagsForCompare = patternWords.findall(tagsArticles)
        for tag in enteredTags:
            for cmpTag in tagsForCompare:  # !!!
                #  print(str(file) + " Файл" + str(tag) + " Тег" + str(cmpTag) + " cmpTag")
                if tag == cmpTag:
                    countHaveTag = countHaveTag + 1
                else:
                    countNoTag = countNoTag + 1

        # if "eq" in listEq and examplePattern.match(file):
        #     listAnd.append(file)

        # find category
        categoryInFile = myDoc.find("./category").text
        if str(category) != "":
            if str(categoryInFile) != str(category):
                countNot = countNot + 1

        # .........
        # check for have countNot or not
        # print(countNot)
        if enteredTags:
            if countNot == 0 and countHaveTag > 0:
                listAnd.setdefault(str(key.rstrip(".xml")), value)
        else:
            if countNot == 0:
                listAnd.setdefault(str(key.rstrip(".xml")), value)
    return listAnd


def makeSort(sortName, dateSort, listAnd, viewSort, request):
    if sortName:
        sortedTuples = sorted(listAnd.items(), key=lambda item: item[1])
        sortedDict = {k: v for k, v in sortedTuples}
        request.session['data'] = sortedDict

    if dateSort:
        dictDate = dict()
        dictWithDateSort = {}
        datePattern = re.compile(r"(\d*\.\d*\.\d*)")
        for filename in listAnd:
            myDoc = etree.parse("xmlWEBApp/xml/" + str(filename) + ".xml")
            dateAndTime = myDoc.find("./DateAndTime").text
            onlyDate = str(datePattern.findall(dateAndTime)).replace("'", "").replace("[", "").replace("]", "")
            day, month, year = str(onlyDate).split(".")
            dateToDate = date(int(year), int(month), int(day))
            dictDate.setdefault(filename, dateToDate)
        listAnd.clear()
        sortedDict = sorted(dictDate.items(), key=lambda x: x[1])
        for key, value in dict(sortedDict).items():  # key - имя файла , value - дата, в список идкет имя без .xml
            myDoc = etree.parse("xmlWEBApp/xml/" + str(key) + ".xml")
            title = myDoc.find("./title").text
            dictWithDateSort.setdefault(key, title)
        request.session['data'] = dictWithDateSort
        # print(sortedDict)

    if viewSort:
        dictWithViewSort = {}
        dictView = dict()
        for filename in listAnd:
            myDoc = etree.parse("xmlWEBApp/xml/" + str(filename) + ".xml")
            views = myDoc.find("./views").text
            if views == "Статья создана вручную":  # При статье созданной вручную, отсюда при созданном вручную не
                # попадало в дальнейший словарь
                views = 0
            try:
                dictView.setdefault(filename, int(views))
            except ValueError:
                pass
        sortedDict = sorted(dictView.items(), key=lambda x: x[1])
        listAnd.clear()
        for key, value in dict(sortedDict).items():
            myDoc = etree.parse("xmlWEBApp/xml/" + str(key) + ".xml")
            title = myDoc.find("./title").text
            dictWithViewSort.setdefault(key, title)
        request.session['data'] = dictWithViewSort


def getCategory():
    categoryList = []
    for root, dirs, files in os.walk("xmlWEBApp/xml"):
        for filename in files:
            myDoc = etree.parse("xmlWEBApp/xml/" + str(filename))
            categoryArticles = myDoc.find("./category").text
            categoryList.append(categoryArticles)
        # print(",".join(tagsList))
    stringTags = ",".join(categoryList)
    patternWords = re.compile("([а-яА-Я0-9_ ]+)")
    readyTags = set(patternWords.findall(stringTags))
    listTags = []
    for tag in readyTags:
        if tag == ' ':
            pass
        else:
            listTags.append(tag)
    return list(listTags)

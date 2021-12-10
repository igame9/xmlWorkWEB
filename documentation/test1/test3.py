from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas
import re

service = Service(r'.\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(r"http://localhost:8000")
driver.implicitly_wait(2)
listData = []

inputNameArticle = driver.find_element(By.XPATH, "//input[@placeholder='Имя статьи для поиска']")
firstDate = driver.find_element(By.ID, "startDate")
secondDate = driver.find_element(By.ID, "endDate")
inputTags = driver.find_element(By.ID, "tags")
choiceCategories = driver.find_element(By.ID, "categories")
sortByVies = driver.find_element(By.XPATH, "//input[@value='viewSort']")

# Enter data 1
try:
    inputNameArticle.send_keys("Лукаш")
    listData.append([f"Ввод данных в поле 'Имя статьи для поиска'",
                     "Отображение введенных данных в поле",
                     f"Данные успешно ввелись и отобразились в поле"])
except:
    listData.append([f"Нажатие левой кнопкой мыши по полю 'Имя статьи для ввода'и ввод в него данных",
                     "Отображение введенных данных в поле",
                     f"Данные не ввелись в поле"])
try:
    firstDate.send_keys("04.11.2021")
    listData.append([f"Ввод данных в поле 'Начальная дата'",
                     "Отображение введенных данных в поле",
                     f"Данные успешно ввелись и отобразились в поле"])
except:
    listData.append([f"Нажатие левой кнопкой мыши по полю 'Начальная дата'и ввод в него данных",
                     "Отображение введенных данных в поле",
                     f"Данные не ввелись ввелись в поле"])

try:
    secondDate.send_keys("13.11.2021")
    listData.append([f"Ввод данных в поле'Конечная дата'",
                     "Отображение введенных данных в поле",
                     f"Данные успешно ввелись и отобразились в поле"])
except:
    listData.append([f"Нажатие левой кнопкой мыши по полю 'Конечная дата'и ввод в него данных",
                     "Отображение введенных данных в поле",
                     f"Данные не ввелись ввелись в поле"])

try:
    inputTags.send_keys("Политика")
    listData.append([f"Ввод данных в поле 'Теги статьи для поиска'",
                     "Отображение введенных данных в поле",
                     f"Данные успешно ввелись и отобразились в поле"])
except:
    listData.append([f"Нажатие левой кнопкой мыши по полю 'Теги статьи для поиска'",
                     "Отображение введенных данных в поле",
                     f"Данные не ввелись ввелись в поле"])

try:
    choiceCategories.click()
    listData.append([f"Нажатие левой кнопкой мыши по полю выпадающему списку с категориями",
                     "Отображение всех доступных категорий",
                     f"Категории успешно отобразились"])
except:
    listData.append([f"Нажатие левой кнопкой мыши по полю выпадающему списку с категориями",
                     "Отображение всех доступных категорий",
                     f"Категории не отобразились"])

try:
    driver.find_element(By.XPATH, "//*[@id='categories']/option[2]").click()
    listData.append([f"Нажатие в открывшемся списки с категориями на категорию 'Политика'",
                     "Отображение выбранной категории",
                     f"Выбранная категория успешно отобразилась"])
except:
    listData.append([f"Нажатие в открывшемся списки с категориями на категорию 'Политика'",
                     "Отображение выбранной категории",
                     f"Выбранная категория не отобразилась"])

try:
    sortByVies.click()
    listData.append([f"Нажатие левой кнопкой мыши на радио кнопку 'Сортировать по просмотрам'",
                     "Отображение черной точки в выбранной сортировке",
                     f"Черная точка отобразилась"])
except:
    listData.append([f"Нажатие левой кнопкой мыши на радио кнопку 'Сортировать по просмотрам'",
                     "Отображение черной точки в выбранной сортировке",
                     f"Черная точка не отобразилась"])

try:
    buttonInput = driver.find_element(By.XPATH, "//input[@type='submit']")
    buttonInput.click()
    listData.append([f"Нажатие левой кнопкой мыши на радио кнопку 'Найти статьи'",
                     "Отображение списка статей",
                     f"Список статей отобразился"])
except:
    listData.append([f"Нажатие левой кнопкой мыши на радио кнопку 'Найти статьи'",
                     "Отображение списка статей",
                     f"Список статей не отобразился"])

# End enter data 1
# Check Articles
listData1 = []
for articles in driver.find_element(By.CLASS_NAME, "list-group"). \
        find_elements(By.XPATH, "(//a[contains(@class,'list-group-item list-group-item-action')])"):
    listData1.append(articles.get_attribute("href"))

regCategories = re.compile(r"Политика")
regNameArticle = re.compile(r"Лукаш")
regTagsArticle = re.compile(r"Политика")

i = 0
for href in listData1:
    i = i + 1
    try:
        driver.get(href)
        listData.append([f"Открытие найденной статьи номер {i}",
                         "Открытие статьи",
                         f"Статья открылась"])
    except:
        listData.append([f"Открытие найденной статьи номер {i}",
                         "Открытие статьи",
                         f"Статья не открылась"])
    categoryInArticle = driver.find_element(By.ID, "category")
    titleInArticle = driver.find_element(By.ID, "title")
    tagsInArticle = driver.find_element(By.ID, "tags")

    # print(tagsInArticle.text)
    # print(regTagsArticle.match(str(tagsInArticle.text)))

    if regCategories.search(str(categoryInArticle.text)) and regNameArticle.search(
            str(titleInArticle.text)) and regTagsArticle.search(str(tagsInArticle.text)):
        listData.append([f"Просмотр данных статьи на предмет корректности относительно искомых",
                         "Данные корректны относительно искомых",
                         f"Данные корректны"])
    else:
        listData.append([f"Просмотр данных статьи на предмет корректности относительно искомых",
                         "Данные корректны относительно искомых",
                         f"Данные не корректны относительно искомых данных"])

dataFrame = pandas.DataFrame(listData, columns=("Действие", "Ожидаемый результат", "Фактический результат"))
dataFrame.to_excel('./test3.xlsx', index=False)
driver.close()

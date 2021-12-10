from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas

service = Service(r'.\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(r"http://localhost:8000")
driver.implicitly_wait(2)
listData = []
listData.append(["Действие", "Ожидаемый результат", "Фактический результат"])

for i in range(20):
    try:
        buttonInput = driver.find_element(By.XPATH, "//input[@type='submit']")
        buttonInput.click()
        try:
            message = driver.find_element(By.XPATH, "//div[text()='Введите какие-нибудь данные для поиска статей']")
            listData.append([f"Нажатие левой кнопкой мыши по кнопке 'Найти статьи' номер {i}",
                             "Получение сообщения о необходимсоти ввода данных для поиска",
                             f"Сообщение номер {i} успешно получено"])
        except:
            listData.append([f"Нажатие левой кнопкой мыши по кнопке 'Найти статьи' номер {i}",
                             "Получение сообщения о необходимсоти ввода данных для поиска", "Сообщение не получено"])
    except:
        listData.append([f"Нажатие левой кнопкой мыши по кнопке 'Найти статьи' номер {i}",
                         "Получение сообщения о необходимсоти ввода данных для поиска", "Кнопка не сработала"])

dataFrame = pandas.DataFrame(listData, columns=("Действие", "Ожидаемый результат", "Фактический результат"))
dataFrame.to_excel('./test2.xlsx', index=False)
driver.close()
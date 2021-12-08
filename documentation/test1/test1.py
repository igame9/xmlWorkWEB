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
i = 1
for _ in range(20):
    if i == 1:
        buttonNext = driver.find_element(By.CLASS_NAME, "likeAButton")
        buttonNext.click()
        i = i + 1
        listData.append(
            [f'Левый клик мышью по кнопке "Следующая страница"', f'Переход на страницу {i}', f'Страница {i} открыта'])
    else:
        try:
            buttonNext = driver.find_element(By.XPATH, "(//a[@class='likeAButton'])[2]")
            buttonNext.click()
            i = i + 1
            listData.append([f'Левый клик мышью по кнопке "Следующая страница"', f'Переход на страницу {i}',
                             f'Страница {i} открыта'])
        except NoSuchElementException:
            listData.append([f'Достигнута последняя страница - {i}', f'Переход на последнюю страницу для теста: {i}',
                             f'Последняя страница {i} открыта'])

j = 21
for _ in range(20):
    if j == 21:
        buttonBack = driver.find_element(By.CLASS_NAME, "likeAButton")
        buttonBack.click()
        j = j - 1
        listData.append(
            [f'Левый клик мыши по кнопку "Предыдущая страница"', f'Переход обратно на страницу {j}',
             f'Страница {j} открыта'])

    try:
        buttonBack = driver.find_element(By.XPATH, "(//a[@class='likeAButton'])[1]")
        buttonBack.click()
        j = j - 1
        listData.append(
            [f'Левый клик мыши по кнопку "Предыдущая страница"', f'Переход обратно на страницу {j}',
             f'Страница {j} открыта'])
    except NoSuchElementException:
        print("Вы на 1 странице!")

dataFrame = pandas.DataFrame(listData, columns=("Действие", "Ожидаемый результат", "Фактический результат"))
dataFrame.to_excel('./test1.xlsx', index=False)

driver.close()

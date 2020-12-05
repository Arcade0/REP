from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.by import By

def next_page(self):
    try:
        self.nextpage = self.wait.until(  # 注意这里不是立即点击的，要判断是否可以立即点击
            EC.element_to_be_clickable((By.XPATH, '//*[@title="Next page of results"]')))
    except TimeoutException:
        self.status = False

arr=[]
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)
browser.implicitly_wait(10)
browser.get("https://www.ncbi.nlm.nih.gov/pubmed/?term=Streptococcus+alactolyticus")
book_a = browser.find_elements_by_class_name('rprtid')
for book in book_a:
    arr.append((book.text)[6:len(book.text)])
print(arr)


def next_page():
    try:
        self.nextpage = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@title="Next page of results"]')))
    except TimeoutException:
        status = False


while True:
    if status:
        next_page()
    else:
        break

book_a = browser.find_elements_by_class_name('rprtid')
for book in book_a:
    arr.append((book.text)[6:len(book.text)])
print(arr)




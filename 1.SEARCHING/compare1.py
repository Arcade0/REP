from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import urllib


class NcbiInfo(object):
    option = webdriver.ChromeOptions()
    browser = webdriver.Chrome()
    start_url = 'https://www.ncbi.nlm.nih.gov/pubmed/'
    wait = WebDriverWait(browser, 10)


    def __init__(self):
        self.url = NcbiInfo.start_url + '30997656'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.file = open('information.txt', 'w')
        self.status = True
        self.yearlist = []

    def click_yearandabstract(self, ):
        self.browser.get(self.url)
        perpage = self.wait.until(EC.element_to_be_clickable((By.XPATH, 'h4//[@class="content_header send_to align_right jig-ncbipopper"]/a')))
        perpage.click()
    def main(self):
        self.click_yearandabstract()

a = NcbiInfo()
a.main()
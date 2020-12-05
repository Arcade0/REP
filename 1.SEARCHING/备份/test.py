# 完整代码如下
import urllib
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class crabInfo(object):
    browser = webdriver.Chrome()
    start_url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term='
    wait = WebDriverWait(browser, 100)

    def __init__(self, keywordlist):
        self.temp = [urllib.parse.quote(i) for i in keywordlist]
        self.keyword = '%2C'.join(self.temp)
        self.title = ' AND '.join(self.temp)
        self.url = crabInfo.start_url + self.keyword
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.file = open('information.txt', 'w')
        self.status = True
        self.yearlist = []

    # 设置初始化
    def click_init(self, ):
        self.browser.get(self.url)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_ds1 > li > ul > li:nth-child(1) > a'))).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//ul[@class="inline_list left display_settings"]/li[3]/a/span[4]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#display_settings_menu_ps > fieldset > ul > li:nth-child(1) > label'))).click()
        print("爬取五年的论文数据，每页显示200条数据......")

    # 获取页面文档
    def get_response(self):
        self.html = self.browser.page_source
        self.doc = etree.HTML(self.html)

    # 获取列表页的论文PMID
    def get_info(self):
        self.baseurl = 'https://www.ncbi.nlm.nih.gov/pubmed/'
        self.art_timeanddoi = self.doc.xpath('//div[@class="rprt"]/div[2]/div[2]/div/dl/dd/text()')
        for pmid in self.art_timeanddoi:
            url_content = self.baseurl + pmid  # 拼接论文详情页的地址
            print(url_content)
            self.browser.get(url_content)  # 进入论文详情页
            self.get_response()  # 进入页面后重新获取页面结构
            self.get_detail(pmid)  # 获取论文的详情信息
            self.browser.back()  # 从论文详情页返回列表页
            self.get_response()

    def get_detail(self, pmid):
        abstract = self.doc.xpath('//div[@class="abstr"]/div/p/text()')  # 获取论文摘要信息
        keywords = self.doc.xpath('//div[@class="keywords"]/p/text()')  # 获取论文keywords信息
        title = self.doc.xpath('//div[@class="rprt abstract"]/h1/text()')  # 获取论文title
        fileName = "/Users/mac/Desktop/pubmed/data/" + str(pmid) + ".txt"  # 打开输出论文信息的.txt文件，每个文件用pmid命名
        result = open(fileName, 'w')
        result.write("[Title]\r\n")
        result.write(''.join(str(i) for i in title))
        result.write("\r\n[Astract]\r\n")
        result.write(''.join(str(i) for i in abstract))
        result.write("\r\n[Keywords]\r\n")
        result.write(''.join(str(i) for i in keywords))
        result.close()
        print(str(pmid) + ".txt书写完毕")

    # 跳转到下一个页面
    def next_page(self):
        try:
            self.nextpage = self.wait.until(  # 注意这里不是立即点击的，要判断是否可以立即点击
                EC.element_to_be_clickable((By.XPATH, '//*[@title="Next page of results"]')))
        except TimeoutException:
            self.status = False

    def main(self):
        self.click_init()  # 页面设置初始化
        time.sleep(3)  # 等待
        self.get_response()  # 获取新页面的页面结构
        count = 0  # 用count来计数总共要爬取的论文数量，初始为0
        while True:
            self.get_info()  # 首先获取当前列表页的论文信息
            self.next_page()  # 进入下一页
            if self.status:  # 判断跳转是否成功
                self.nextpage.click()  # 执行跳转的点击操作
                self.get_response()
            else:
                print("跳转未成功......")
                break
            count = count + 1
            print(str(count))
            if count == 2:  # 可以根据需要修改count的值，这里只爬取20000条
                break


if __name__ == '__main__':
    arr = ['tuberculosis']  # arr保存需要查找的论文关键字，如cancer等
    a = crabInfo(arr)
    print(str(arr))
    a.main()
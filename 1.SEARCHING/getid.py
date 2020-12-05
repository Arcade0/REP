import urllib.request
from bs4 import BeautifulSoup
import xlwt
import pubmed
import readkey

def replaceSpace(s):#空格变20%
    # write code here
    sr = ''
    for t in s:
        if t == ' ':
            sr += '%20'
        else:
            sr += t
    return sr

hanghao = 0
while hanghao < readkey.readrows():#读取关键词数量并循环
   hanghao = hanghao + 1
   key="https://www.ncbi.nlm.nih.gov/pubmed/?term="+readkey.readkey(hanghao)#读取关键词
   print(key)#是否读取到关键词
   res = urllib.request.urlopen(replaceSpace(key))#获取网址
   soup = BeautifulSoup(res,"lxml")
   book_div = soup.find(attrs={"id":"maincontent"})
   book_a = book_div.findAll(attrs={"class":"rprtid"})#读取pmid
   book1 = xlwt.Workbook()#新建一个excel
   sheet = book1.add_sheet('case1_sheet')#添加一个sheet页
   row = 0
   for book in book_a:
         book.dd.string="https://www.ncbi.nlm.nih.gov/pubmed/"+book.dd.string
         sheet.write(row,0,book.dd.string)
         print(book.dd.string)
         row = row+1
   book1.save(readkey.readkey(hanghao)+'.xlsx')#pmid保存到excel
   pubmed.abstarct(hanghao)#下载关键词

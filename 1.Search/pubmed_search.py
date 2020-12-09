import numpy as np
from Bio import Medline, Entrez  # 一般是通过BioPython的Bio.Entrez模块访问Entrez
from collections import Counter
import os
import json

Entrez.email = "（xinzhuo12345678@163.com）"  # 应用自己的账号访问NCBI数据库

# 此处需将服务器协议指定为1.0，否则会出现报错。http.client.IncompleteRead: IncompleteRead(0 bytes read)
# 服务器http协议1.0，而python的是1.1，解决办法就是指定客户端http协议版本
import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

def mk_dir(file_path):

    folder = os.path.exists(file_path)
    if not folder:
        os. makedirs(file_path)

def query(spec_l, keyword, 
          date="(1900/01/01[Date - Publication] : 2021/12/31[Date - Publication])", 
          ret_max=100, step=100, 
          fur_query=False):

    """
    Entrez 是一个检索系统，可以用其访问NCBI数据库，比如说PubMed，GenBank，GEO等。
    获得有关 global PBDE 的所有文献的PubMed IDs
    """

    for spec in spec_l:
        
        mk_dir("output/%s/%s" % (spec.split(" ")[0], spec.replace(" ", "_"))) # 保存格式 类/种名
        term_l = [spec + " AND " + ele for ele in keyword]
        term_l.append(spec)
        
        for term in term_l:
        
            handle_0 = Entrez.esearch(
                db = "pubmed", 
                term = term + " AND " + date,
#                 ptyp="Review", 
                usehistory="y", 
                retmax=ret_max)

            record = Entrez.read(handle_0)  # 获取检索条件的所有文献
            idlist = record["IdList"]  # 提取出文献id
            webenv = record['WebEnv']
            query_key = record['QueryKey']
            No_Papers = len(idlist)

            total = No_Papers
            print (term + " Total: ", record["Count"])
            
            with open("output/%s/%s/%s.txt" % (
                spec.split(" ")[0], 
                spec.replace(" ", "_"), 
                term.replace(" ", "_")), "w") as f: # save pmid
                
                for ele in idlist:
                    
                    f.write(ele + "\n")
                
                f.close()

            if fur_query==True:
                
                dic = {}
                
                for start in range(0, total, step):
                    
                    print("Download record %i to %i" % (start + 1, int(start + step)))
                    handle_1 = Entrez.efetch(
                        db="pubmed", retstart=start, 
                        rettype="medline", retmode="text",
                        retmax=step, webenv=webenv, 
                        query_key=query_key)  # 获取上述所有文献的PubMed IDs
                    records = Medline.parse(handle_1)
                    records = list(records)
                    dic.update({ele["PMID"]:ele for ele in records})

                with open("output/%s/%s/%s.json" % (
                    spec.split(" ")[0], 
                    spec.replace(" ", "_"), 
                    term.replace(" ", "_")), 'w') as f: # save json file
        
                        js = json.dumps(dic)
                        f.write(js)
                        f.close()
                    
if __name__ == "__main__":
    spec_l = ["Corynebacterium accolens"]
    keyword = ["pneumonia", "bronchitis", "lung", 
           "pulmonary", "respiratory", "infection", 
           "empyema", "abscess"]
    date = "(1900/01/01[Date - Publication] : 2021/12/31[Date - Publication])"
    query(spec_l, keyword,
          date, 
          ret_max=100, step=100, 
          fur_query=False)
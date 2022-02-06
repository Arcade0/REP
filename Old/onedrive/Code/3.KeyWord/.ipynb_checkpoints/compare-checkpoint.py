import os
import numpy as np
import pandas as pd
import json 
from collections import Counter
from highlight import replace_html_tag, save_html
from copy import deepcopy
import importlib

def mk_dir(file_path):

    folder = os.path.exists(file_path)
    if not folder:
        os. makedirs(file_path)

def compare(input_path, output_path, keyword, keyp="Mesh"):

    # 建立物种大类列表
    sp_l = [ele for ele in os.listdir(input_path) if "_done" not in ele]
    sp_l = [ele for ele in sp_l if ".ipynb" not in ele]

    for sp in sp_l:
    
        # 建立这个大类中物种列表
        print(sp)
        spec_l = [ele for ele in os.listdir("%s/%s" % (input_path, sp)) if ".ipynb" not in ele]
            
        for spec in spec_l:
            
            # 建立这个物种的三种搜索结果json文件列表
            file_l = [ele for ele in os.listdir("%s/%s/%s" % (input_path, sp, spec)) if ".json" in ele]
            
            if keyp == "Mesh": # 筛选1

                file_l = [ele for ele in file_l if "Mesh" in ele]
                file_l.append(spec + ".json")
            
            for file in file_l:
                
                # 读取json文件中的paper并建立列表
                input_name = "%s/%s/%s/%s" % (input_path, sp, spec, file)
                data_l = json.load(open("%s" % input_name,'r'))
                
                for paper in data_l:
                    
                    # 检查这个paper是否已经对比完成
                    anno_folder = "%s/%s/%s/%s" % (output_path, sp, spec, file.replace(".json", ""))
                    chek = os.path.exists("%s/%s.htmll" %(anno_folder, paper["id"])) # wrong for test
                    if not chek:

                        # 读取pubtator的注释
                        title = paper["passages"][0]["text"]
                        ab = paper["passages"][1]["text"]
                        full = "TITLE:%s ABSTRACT:%s" % (title, ab)
                        sub = [
                            "TITLE:", "ABSTRACT", "BACKGROUND:", "METHOD:", "METHODS:", "FINGDING", 
                            "FINDINGS:", "RESULT", "RESULTS:", 
                            "CONCLUSION", "CONCLUSIONS:", "OBJECTIVE:", "OBJECTITVES"]
                        key_l = [word for word in keyword["LungRelated"] if word in full]

                        if spec.replace("_", " ") in full: # 筛选2
            
                            if len(key_l) > 0: # 筛选3
                                
                                spec_key = deepcopy(keyword)
                                spec_key["LungRelated"].append(spec.replace("_", " "))

                                for word in sub:

                                    full = full.replace(word, "<p>%s" % word)

                                # read title annotation
                                title_anno = paper["passages"][0]["annotations"]
                                title_disease_l = [i['text'] for i in title_anno if i['infons']['type'] == 'Disease']
                                title_gene_l = [i['text'] for i in title_anno if i['infons']['type'] == 'Gene']
                                title_species_l = [i['text'] for i in title_anno if i['infons']['type'] == 'Species']

                                ab_anno = paper["passages"][1]["annotations"]
                                full_disease_l = title_disease_l + [i['text'] for i in ab_anno if i['infons']['type'] == 'Disease']
                                full_gene_l = title_gene_l + [i['text'] for i in ab_anno if i['infons']['type'] == 'Gene']
                                full_species_l = title_species_l + [i['text'] for i in ab_anno if i['infons']['type'] == 'Species']
                                full_che_l = title_species_l + [i['text'] for i in ab_anno if i['infons']['type'] == 'Chemical']

                                full_text = "https://pubmed.ncbi.nlm.nih.gov/%s/" % (paper["id"])
                                full_text_link = '<a href="%s">For Full Text</a>' % full_text

                                # Compare it with Keyword
                                full_ls = [[key, replace_html_tag(full, spec_key[key])] for key in spec_key.keys()]
                                full_ls.append(["Disease", replace_html_tag(full, full_disease_l)])
                                full_ls.append(["Species", replace_html_tag(full, full_species_l)])
                                # full_ls.append(["Gene", replace_html_tag(full, full_gene_l)])
                                # full_ls.append(["Chemical", replace_html_tag(full, full_che_l)])
                                full_ls.append(["Full Text", full_text_link])
                                
                                # 创建文件夹用以保存medID的对比结果
                                mk_dir(anno_folder)
                                save_html(full_ls, "%s/%s" %(anno_folder, paper["id"]))
                                # print("%s(%s) is a molecular paper" % (title, paper["id"]))
                                
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                    

if __name__ == "__main__":
    keyword = json.load(open("keyword.json", "r"))
    input_path = "../2.PubTator/output"
    output_path = "output"
    compare(input_path, output_path, keyword)
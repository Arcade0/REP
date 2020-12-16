import os
import numpy as np
import pandas as pd
import json 
from collections import Counter
import SubmitPMIDList
import importlib
importlib.reload(SubmitPMIDList)
import time
from random import randint


def mk_dir(file_path):

    folder = os.path.exists(file_path)
    if not folder:
        os. makedirs(file_path)

def pubtator(input_path, output_path):

    sp_l = [ele for ele in os.listdir(input_path) if ".ipynb" not in ele]

    for sp in sp_l:

        print(sp)

        spec_l = [ele for ele in os.listdir("%s/%s" % (input_path, sp)) if ".ipynb" not in ele]

        for spec in spec_l:

            file_l = [ele for ele in os.listdir("%s/%s/%s" % (input_path, sp, spec)) if ".txt" in ele]
            
            for file in file_l:

                input_name = "%s/%s/%s/%s" % (input_path, sp, spec, file)
                output_name = "%s/%s/%s/%s" % (output_path, sp, spec, file)
                mk_dir("%s/%s/%s" % (output_path, sp, spec))
                
                chek = os.path.exists(output_name.replace(".txt", ".json"))

                if not chek:
                    
                    print(file)
                    
                    SubmitPMIDList.SubmitPMIDList(input_name, "biocjson", output_name, "")   
                    time.sleep(randint(5, 15))

                    # convert pubtator result to json file 
                    with open('%s' % output_name, 'r') as f:
                        
                        data_t = f.read()
                        data_t = "[" + data_t.replace("\n", ",").strip(",") + "]"
                        f.close()                    

                    with open('%s' % output_name.replace("txt", "json"), 'w') as f:
                        
                        f.write(data_t)
                        f.close()
                        
                else:
                    pass

if __name__ == "__main__":
    input_path = "../1.Search/output"
    output_path = "output"
    pubtator(input_path, output_path)

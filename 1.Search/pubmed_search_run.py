import numpy as np
import pandas as pd
import json
import importlib
import pubmed_search
importlib.reload(pubmed_search)

keyword = json.load(open("keyword.json", "r"))

pubmed_search.query(input_path="input/Virology/spec_cob",
                    output_path="output/Virology/",
                    keyword=keyword["Mesh"],
                    ret_max=100,
                    step=100,
                    fur_query=False)

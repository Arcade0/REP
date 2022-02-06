import os
import numpy as np
import pandas as pd
import json
from collections import Counter
import importlib
import pubtator

importlib.reload(pubtator)

input_path = "../1.Search/output/Virology/"
output_path = "output/Virology/"
pubtator.pubtator(input_path, output_path)
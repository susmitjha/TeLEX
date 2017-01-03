import numpy as np
import pandas as pd

def readtracefile(filename):
    data = pd.read_csv(filename)
    return data

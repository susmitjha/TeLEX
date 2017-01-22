import numpy as np
import pandas as pd

def readtracefile(filename):
    #data = pd.read_csv(filename)
    df_test = pd.read_csv(filename, nrows=100)
    float_cols = [c for c in df_test if df_test[c].dtype == "float64"]
    float32_cols = {c: np.float32 for c in float_cols}
    data = pd.read_csv(filename, engine='c', dtype=float32_cols)
    if data.columns[0]!='time':
        print("The name of first column of trace in {} must be \'time\'. Can't read this trace. Quitting ....\n".format(filename))
        quit()
    data1 = {}
    for colname in data:
        data1[colname] = {}
        for i in range(0,len(data)):
            data1[colname][data["time"][i]] = data[colname][i]
    return data1

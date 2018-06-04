import os
import pandas as pd
file = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2017-050118.txt"
path = pd.read_csv(file, header=None)
print(path)
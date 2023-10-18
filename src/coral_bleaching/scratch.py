import json
import pandas as pd

f = open("classification.json")
classification = json.load(f)

with open ("coral_bleaching.csv", "r++") as dataset:
    data = pd.read_csv("./coral_bleaching.csv")
    column_names = pd.read_csv("coral_bleaching.csv", skiprows=1, encoding='ISO-8859-1')
    print(column_names)

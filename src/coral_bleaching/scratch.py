import pandas as pd
import csv
import json

data = pd.read_csv("./coral_bleaching.csv")

f = open("classification.json")
classification = json.load(f)

print(data["CORAL_FAMILY"])
families = data["CORAL_FAMILY"].tolist()
for i in families:
    if i == None:
        break
    for j in classification:
        if j["family"] == i:
            print("Correct")
        elif i in j["family_typos"]:
            print("Typo")
        elif i in j["genus"] or i in j["species"] or i in j["species_typos"]:
            print("Misinformation")

import json

file = open('DataPreprocessing_MMdetection\i0273157.json')
jsonString = json.load(file)

jsonArray = jsonString.get("annotation")[0]

print(jsonArray.get("shape"))
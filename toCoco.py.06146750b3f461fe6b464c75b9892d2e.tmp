import json

js = '{"annotation":[{"shape":"circle","color":"red","kind":"normal","box":[1174,376,1215,415],"text":"70","type":"restriction","class":"traffic_sign"}],"image":{"filename":"i0273157.jpg","imsize":[1920,1200]}}'
jsonObject = json.loads(js)
jsonArray = jsonObject.get("annotation")[0]

print(jsonArray.get("shape"))
# coding:utf-8
import json
import os
 
# 파일 리스트 불러오기, 0: test, 1: train
name = ["test", "train"]
originAnnoFilesDir = ["sycData\\test_road_information\\label\\", "sycData\\train_road_information\\label\\"]
# originAnnoFilesDir = ["sample\\test\\label\\", "sample\\train\\label\\"]
originAnnoFilesList = [os.listdir(originAnnoFilesDir[0]), os.listdir(originAnnoFilesDir[1])]
 
# test, train 공통부분
categoriyDict = {"traffic_sign": 0, "traffic_light": 1, "traffic_information":2} # 2는 사용 x
common_categories = [
  {"id": 0, "name": "traffic_sign"},
  {"id": 1, "name": "traffic_light"},
  {"id": 2, "name": "traffic_information"}
] # 2는 사용 x
 
for i in range(len(originAnnoFilesList)): # 0: test, 1: train
    CocoDict = {} # coco 데이터셋이 될 딕셔너리
   
    # 공통부분 처리
    CocoDict["categories"]  = common_categories
 
    # 다음 for문에서 채울 정보들
    cocoImgs = []
    cocoAnnos = []
    annotationCount = 0; # annotation 각 원소 id 부여
    for imgId in range(len(originAnnoFilesList[i])): # 원본 annotation 파일 불러오기, j는 이미지 id
        with open(originAnnoFilesDir[i] + originAnnoFilesList[i][imgId], encoding="utf-8-sig") as originData:
            jsonData = json.load(originData) # 파싱
 
            # 이미지 정보 저장
            imgPath = originAnnoFilesList[i][imgId].replace(".json", ".jpg")
            images = {
                "file_name": jsonData["image"]["filename"],
                "width": jsonData["image"]["imsize"][0],
                "height": jsonData["image"]["imsize"][1],
                "id": imgId
            }
            cocoImgs.append(images)
 
            # 여러개 annotation 정보 하나씩 가공
            for k in range(len(jsonData["annotation"])): # 원본데이터 안에서 하나의 annotation 정보 처리
                categoryId = categoriyDict[jsonData["annotation"][k]["class"]]
                if categoryId != 2:
                    width = jsonData["annotation"][k]["box"][2]-jsonData["annotation"][k]["box"][0]
                    height = jsonData["annotation"][k]["box"][3]-jsonData["annotation"][k]["box"][1]
                    area = width*height
                    bbox = [
                        jsonData["annotation"][k]["box"][0],
                        jsonData["annotation"][k]["box"][1],
                        width,
                        height
                    ]
                    annotation = {
                        "segmentation": [[]],
                        "image_id": imgId,
                        "bbox": bbox,
                        "category_id": categoryId,
                        "id": annotationCount,  
                        "area": area,
                        "iscrowd": 0,
                    }
                    cocoAnnos.append(annotation)
                    annotationCount += 1
 
    CocoDict["images"] = cocoImgs # coco 데이터 images 부분
    CocoDict["annotations"] = cocoAnnos # coco 데이터 annotations 부분
 
    # json 파일 저장
    with open("./" + name[i] + "Coco.json", 'w') as coco :
        json.dump(CocoDict, coco, ensure_ascii=False)
        print("finish making ./" + name[i] + "Coco.json")
        print(name[i] + "annotation count: " + str(annotationCount))
        print(name[i] + "image count: " + str(len(originAnnoFilesList[i])))

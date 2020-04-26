# -*- coding: utf-8 -*-
# +
from shapely.geometry import Polygon
from PIL import Image, ImageDraw
from tqdm import tqdm
import random
import json
import os


boat_dict = {}
with open("boat_labels.json") as json_file:
    json_data = json.load(json_file)
    for data in json_data:
        boat_dict[data] = json_data[data]


image_dict = {}
with open('labels.json') as json_file:
    json_data = json.load(json_file)
    for data in json_data["features"]:
        image_id = data["properties"]["image_id"]
        type_id = data["properties"]["type_id"]
        try:
            image_dict[image_id]["type_id"].append(type_id)
        except:
            image_dict[image_id] = {}
            image_dict[image_id]["type_id"] = []
            image_dict[image_id]["type_id"].append(type_id)
            
random_boat_num = []

S = [0 for i in range(200)]

for key in image_dict.keys():
    n = len(image_dict[key]['type_id'])
    S[n] += 1
for i in range(200):
    for j in range(S[i]):
        random_boat_num.append(i)

boat_path = "Boat3/"
sea_list = ['sea', 'sea2', 'sea3', 'sea4', 'sea6', 'sea7', 'sea8']
boats_name = os.listdir(boat_path)
boat_length = len(boats_name)
labeling_dict = {}

for Gnum in tqdm(range(6000)):
    boat_num = random.randrange(0,len(random_boat_num))
    boat_num = random_boat_num[boat_num] + 1 #원본 데이터의 비율에 맞게 보트 생성
    sea_type = random.randrange(0,len(sea_list))
    sea_idx = random.randrange(0,50)
    
    sea_dir = "./../SinGAN/Output/RandomSamples_ArbitrerySizes/"
    sea_dir += sea_list[sea_type]
    sea_dir += "/scale_v=6.000000_scale_h=6.000000/"
    sea_dir +=  (str(sea_idx) + ".png")

    sea_im = Image.open(sea_dir).convert("RGBA")
    polygons = []
    class_ids = []
    bounding_boxs = []
    is_continue = False
    for i in range(boat_num):
        boat_idx = random.randrange(0, boat_length)
        boat_im = Image.open(boat_path + boats_name[boat_idx])
        posX = random.randrange(0,1350) #어디서부터 배를 생성할 것인지
        posY = random.randrange(0,1350)
        try:
            bounding_box = list(map(float, boat_dict[boats_name[boat_idx]].split(',')))
        except KeyError:
            continue
        for i in range(0,8,2):
            bounding_box[i] += posX
            bounding_box[i+1] += posY
        temp_polygon = Polygon([(bounding_box[0],bounding_box[1]), (bounding_box[2],bounding_box[3]),
                        (bounding_box[4],bounding_box[5]), (bounding_box[6],bounding_box[7])])
        is_continue = False
        for i, P in enumerate(polygons): # 겹치는 부분이 있으면 break해줄 것임
            Overlap = temp_polygon.intersection(P).area #겹치는 부분
            if Overlap > 0.1:
                is_continue = True
                break

        if is_continue:
            continue
        polygons.append(temp_polygon)                       # polygon 배열에 현재 polygon을 추가시킴 
        sea_im.paste(boat_im,(posX, posY), boat_im)         # sea_im에 boat이미지를 저장시킴
        class_ids.append(int(boats_name[boat_idx].split('_')[0])) #class id를 저장
        bounding_boxs.append(bounding_box)
            


    save_im_name = str(Gnum) + '.png'
    labeling_dict[save_im_name] = {}
    labeling_dict[save_im_name]["class_id"] = class_ids
    labeling_dict[save_im_name]["bounding_box"] = bounding_boxs
    sea_im.save("GeneratingImages/GenerateImage2/images/" + save_im_name)
# except:
#     print("SOMETHING ERROR")
#     pass
with open("GeneratingImages/GenerateImage2/labels.json", "w") as json_file:
    json.dump(labeling_dict, json_file)
    
# import json
# from shapely.geometry import Polygon
# from PIL import Image, ImageDraw
# from tqdm import tqdm
# import random
# import json
# import os

# boat_dict = {}
# with open("boat_labels.json") as json_file:
#     json_data = json.load(json_file)
#     for data in json_data:
#         print(data)
#         boat_dict[data] = json_data[data]


# from matplotlib import pyplot as plt
# str_n = "4_12.png"
# im = Image.open("Boat3/" + str_n)
# arr = list(map(float, boat_dict[str_n].split(',')))
# arr

# X = [arr[i] for i in range (0,8,2)]
# Y = [arr[i] for i in range (1,8,2)]
# plt.plot(X,Y)
# plt.imshow(im)



"""

rotate code

"""

# from shapely.geometry import Polygon
# from PIL import Image, ImageDraw
# from tqdm import tqdm
# import random
# import json
# import os
# import math

# def rotate_arr(lists, angle):
#     X = [lists[i] for i in range(0, 8,2)] + [lists[0]]
#     Y = [lists[i] for i in range(1,8,2)] + [lists[1]]
#     pi = -angle / 180 * math.pi
#     meanX = (max(X) + min(X))/2
#     meanY = (max(Y) + min(Y))/2
#     X = [X[i] - meanX for i in range(len(X))]
#     Y = [Y[i] - meanY for i in range(len(Y))]
#     X_ = [X[i]*math.cos(pi) - Y[i]*math.sin(pi) for i in range(5)]
#     Y_ = [X[i]*math.sin(pi) + Y[i]*math.cos(pi) for i in range(5)]
#     X_ = [X_[i] + meanX for i in range(len(X_))]
#     Y_ = [Y_[i] + meanY for i in range(len(Y_))]    

#     return X_, Y_

# boat_dict = {}
# with open("boat_labels.json") as json_file:
#     json_data = json.load(json_file)
#     for data in json_data:
#         boat_dict[data] = json_data[data]


# image_dict = {}
# with open('labels.json') as json_file:
#     json_data = json.load(json_file)
#     for data in json_data["features"]:
#         image_id = data["properties"]["image_id"]
#         type_id = data["properties"]["type_id"]
#         try:
#             image_dict[image_id]["type_id"].append(type_id)
#         except:
#             image_dict[image_id] = {}
#             image_dict[image_id]["type_id"] = []
#             image_dict[image_id]["type_id"].append(type_id)
            
# random_boat_num = []

# S = [0 for i in range(200)]

# for key in image_dict.keys():
#     n = len(image_dict[key]['type_id'])
#     S[n] += 1
# for i in range(200):
#     for j in range(S[i]):
#         random_boat_num.append(i)

# boat_path = "Boat3/"
# sea_list = ['sea', 'sea2', 'sea3', 'sea4', 'sea6', 'sea7', 'sea8']
# boats_name = os.listdir(boat_path)
# boat_length = len(boats_name)
# labeling_dict = {}

# for Gnum in tqdm(range(3)):
#     boat_num = random.randrange(0,len(random_boat_num))
#     boat_num = random_boat_num[boat_num] + 40 #원본 데이터의 비율에 맞게 보트 생성
#     sea_type = random.randrange(0,len(sea_list))
#     sea_idx = random.randrange(0,50)
    
#     sea_dir = "./../SinGAN/Output/RandomSamples_ArbitrerySizes/"
#     sea_dir += sea_list[sea_type]
#     sea_dir += "/scale_v=6.000000_scale_h=6.000000/"
#     sea_dir +=  (str(sea_idx) + ".png")

#     sea_im = Image.open(sea_dir).convert("RGBA")
#     polygons = []
#     class_ids = []
#     bounding_boxs = []
#     is_continue = False
#     for i in range(boat_num):
#         boat_idx = random.randrange(0, boat_length)
#         boat_im = Image.open(boat_path + boats_name[boat_idx])
        
#         posX = random.randrange(0,1350) #어디서부터 배를 생성할 것인지
#         posY = random.randrange(0,1350)
#         try:
#             angle = random.randrange(0,360)
#             boat_im = boat_im.rotate(angle)
#             bounding_box = list(map(float, boat_dict[boats_name[boat_idx]].split(',')))
#             X_, Y_ = rotate_arr(bounding_box, angle)
#         except KeyError:
#             continue
            
#         X_ = [X_[i] + posX for i in range(len(X_))]
#         Y_ = [Y_[i] + posY for i in range(len(Y_))]

#         temp_polygon = Polygon([(X_[0],Y_[0]), (X_[1],Y_[1]),
#                         (X_[2],Y_[2]), (X_[3],Y_[3])])
#         is_continue = False
#         for i, P in enumerate(polygons): # 겹치는 부분이 있으면 break해줄 것임
#             Overlap = temp_polygon.intersection(P).area #겹치는 부분
#             if Overlap > 0.1:
#                 is_continue = True
#                 break

#         if is_continue:
#             continue
#         polygons.append(temp_polygon)                       # polygon 배열에 현재 polygon을 추가시킴 
#         sea_im.paste(boat_im,(posX, posY), boat_im)         # sea_im에 boat이미지를 저장시킴
#         class_ids.append(int(boats_name[boat_idx].split('_')[0])) #class id를 저장
#         bounding_box = [X_[0], Y_[0], X_[1], Y_[1], X_[2], Y_[2], X_[3], Y_[3]]
#         bounding_boxs.append(bounding_box)
            


#     save_im_name = str(Gnum) + '.png'
#     labeling_dict[save_im_name] = {}
#     labeling_dict[save_im_name]["class_id"] = class_ids
#     labeling_dict[save_im_name]["bounding_box"] = bounding_boxs
#     sea_im.save("GeneratingImages/GenerateImage2/images/" + save_im_name)
# # except:
# #     print("SOMETHING ERROR")
# #     pass
# with open("GeneratingImages/GenerateImage2/labels.json", "w") as json_file:
#     json.dump(labeling_dict, json_file)



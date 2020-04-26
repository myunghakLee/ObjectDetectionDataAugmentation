# -*- coding: utf-8 -*-
"""DataPreprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j7K4uQix4hVy2AkPXKTNY-fYSQQJRDDF
"""
from tqdm import tqdm
import argparse
import json
import cv2
import json
from PIL import Image
import random

parser = argparse.ArgumentParser(description='PreProcessing')
parser.add_argument('--image_size', type=int, default=3000)
parser.add_argument('--crop_size', type=int, default=600, choices=[300, 500, 600, 1000, 1200, 1500])
parser.add_argument('--step_size', type=int, default=300, choices=[100, 200, 300, 500, 600, 700, 800])
parser.add_argument('--save_path', type=str, default='prac')
parser.add_argument('--image_path', type=str, default='images_original')
parser.add_argument('--json_file', type=str , default='labels_original.json')
parser.add_argument('--noise_include_ratio', type=float, default=0.01)
parser.add_argument('--print_frequency', type=int, default=50)

args = parser.parse_args()
crop_size = args.crop_size
step_size = args.overlap_size
image_size = args.image_size
save_path = args.save_path +'/'
image_path = args.image_path + '/'
Noise_include_ratio = args.noise_include_ratio
PrintFrequency = args.print_frequency

f = open(save_path + "option.txt", 'w')
option_data = ""
option_data += "crop_size : " + str(crop_size) + '\n'
option_data += "overlap_size : " + str(overlap_size) + '\n'
option_data += "save_path : " + str(save_path) + '\n'
option_data += "image_path : " + str(image_path) + '\n'
option_data += "Noise_include_ratio : " + str(Noise_include_ratio) + '\n'
option_data += "PrintFrequency : " + str(PrintFrequency) + '\n'
f.write(option_data)
f.close()

def Is_exceed(bbox, temp_image):   # temp_image = [xmin, ymin, xmax, ymax]
  boxs = []
  exceed = []
  for i, box in enumerate(bbox):
    Xmin = min(box[0],box[2],box[4],box[6])
    Xmax = max(box[0],box[2],box[4],box[6])
    Ymin = min(box[1],box[3],box[5],box[7])
    Ymax = max(box[1],box[3],box[5],box[7])
    # if (Xmax < temp_image[0] or Xmin > temp_image[2] or 
    #     Ymax < temp_image[1] or Ymin > temp_image[3]):
    #   not_excced[i] = False
    #   boxs.append("")
    if ((temp_image[0] < Xmin < temp_image[2]) and (temp_image[0] < Xmax < temp_image[2]) and
                                                   (temp_image[1] < Ymin < temp_image[3]) and 
                                                   (temp_image[1] < Ymax < temp_image[3])):      #bounding box가 완전히 사진 안에 들어가는 경우
      exceed.append(False) 
      boxs.append([box[0] - temp_image[0] , box[1] - temp_image[1],
                   box[2] - temp_image[0] , box[3] - temp_image[1],
                   box[4] - temp_image[0] , box[5] - temp_image[1],
                   box[6] - temp_image[0] , box[7] - temp_image[1]])
    else:
      exceed.append(True) 
      boxs.append([None])

  Info = {}
  Info['IsExceed'] = exceed
  Info['Box'] = boxs
  return Info



image_dic = {}
with open(args.json_file) as json_file:
  json_datas = json.load(json_file)
  for json_data in json_datas['features']:
    image_id = json_data['properties']['image_id']
    box_position = json_data['properties']['bounds_imcoords']
    box_position = box_position.split(',')
    box_position = [float(i) for i in box_position]
    try:
      image_dic[image_id]['box_position'].append(box_position)
      image_dic[image_id]['type_id'].append([json_data['properties']['type_id']])
    except KeyError:
      image_dic[image_id] ={}
      image_dic[image_id]['box_position'] = []
      image_dic[image_id]['box_position'].append(box_position)
      image_dic[image_id]['type_id'] = []
      image_dic[image_id]['type_id'].append([json_data['properties']['type_id']])

json_str = {}
json_str["features"] = []
json_str["type"] = "FeatureCollection"
for i, key in enumerate(tqdm(image_dic.keys())):
#   if (i+1) % PrintFrequency == 0:
#     print("num : " , i , "complete")
  
  img = Image.open(image_path + key)
  minX, minY, maxX, maxY = 0, 0, crop_size, crop_size
  while True:
        
    if maxY > image_size:
      break
    if maxX > image_size:
      minX = 0
      maxX = crop_size
      maxY += overlap_size
      minY += overlap_size
      continue
    
    ExceedInfo = Is_exceed(image_dic[key]['box_position'], [minX, minY, maxX, maxY])
    is_save_ok = True
    for i in range(len(ExceedInfo['IsExceed'])):
      temp_json_str = {}
      temp_json_str["properties"] ={}
      if(not ExceedInfo['IsExceed'][i] or random.random() < Noise_include_ratio):

        if is_save_ok:
            area = (minX, minY, maxX, maxY)
            cropped_img = img.crop(area)
            file_name = str(key.split('.')[0]) + "_" + str(minY) + "_" + str(minX) +"_" + str(maxY) + "_" + str(maxX) + ".png"
            path = save_path + file_name
            cropped_img.save(path)
            is_save_ok = False
        
          
        if not ExceedInfo['IsExceed'][i]:
          temp_json_str["properties"]["bounds_imcoords"] = ExceedInfo['Box'][i]
          temp_json_str["properties"]["startX"] = minX
          temp_json_str["properties"]["startY"] = minY
          temp_json_str["properties"]["image_size"] = crop_size
          temp_json_str["properties"]["type_id"] = int(image_dic[key]['type_id'][i][0])
          temp_json_str["properties"]["pre_image_id"] = key
          temp_json_str["properties"]["image_id"] = file_name
        else:
          temp_json_str["properties"]["bounds_imcoords"] =None
          temp_json_str["properties"]["startX"] = minX
          temp_json_str["properties"]["startY"] = minY
          temp_json_str["properties"]["image_size"] = crop_size
          temp_json_str["properties"]["type_id"] = None
          temp_json_str["properties"]["pre_image_id"] = key
          temp_json_str["properties"]["image_id"] = file_name
        json_str["features"].append(temp_json_str)
    maxX+=overlap_size
    minX+=overlap_size
    if(maxX - minX != crop_size):
        print(minX, "@@@@@@@@@@@@@@@@@@@@@@@@@", maxX)

with open(save_path + "lables.json", "w") as json_file:
  json.dump(json_str, json_file, indent="\t")



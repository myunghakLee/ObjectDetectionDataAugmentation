import json
import cv2
import numpy as np
from PIL import Image, ImageDraw
from tqdm.notebook import tqdm
import os


image_dict = {}

with open('labels.json') as json_file:
    json_data = json.load(json_file)
    for data in json_data["features"]:
        image_id = data["properties"]["image_id"]
        imcoords = list(map(float, data["properties"]["bounds_imcoords"].split(',')))
        type_id = data["properties"]["type_id"]
        try:
            image_dict[image_id]["bounding_box"].append(imcoords)
            image_dict[image_id]["type_id"].append(type_id)
        except:
            image_dict[image_id] = {}
            image_dict[image_id]["bounding_box"] = []
            image_dict[image_id]["type_id"] = []
            image_dict[image_id]["bounding_box"].append(imcoords)
            image_dict[image_id]["type_id"].append(type_id)

category_num = [0,0,0,0]
file_list = os.listdir("Object")

# +
save_dict = {}
zero_arr = np.array([0,0,0,0])

for image_number in tqdm(range(len(file_list))):
    im = Image.open("Object/" + file_list[image_number]).convert("RGBA")
    for i in range(len(image_dict[file_list[image_number]]["bounding_box"])):
        boxX = [image_dict[file_list[image_number]]["bounding_box"][i][j] for j in range(-2,8,2)] 
        boxY = [image_dict[file_list[image_number]]["bounding_box"][i][j] for j in range(-1,8,2)] 
        if min(boxX) < 0 or min(boxY) < 0 or max(boxX) > 3000 or max(boxY) > 3000:
            continue


        type_id = image_dict[file_list[image_number]]["type_id"][i]

        imArray = np.asarray(im)
        polygon = []
        for j in range(len(boxX)):
            T = (int(boxX[j]),int(boxY[j]))
            polygon.append(T)

        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
        mask = np.array(maskIm)
        # assemble new image (uint8: 0-255)
        newImArray = np.empty(imArray.shape,dtype='uint8')

        newImArray[:,:,:3] = imArray[:,:,:3]
        newImArray[:,:,3] = mask*255

    #    newIm = Image.fromarray(newImArray, "RGBA")


        data = []
        for j in range(int(min(boxY)), int(max(boxY))):
            T = []
            for k in range(int(min(boxX)), int(max(boxX))):
                T.append(list(newImArray[j][k]))
            data.append(T)
        data = np.array(data)
        S1 = sum(data[0][0])
        if sum(data[0][0]) == 0 or sum(data[0][-1]) == 0 or sum(data[-1][0])  ==0 or sum(data[-1][-1]) == 0:
            print(str(type_id) + "_"+str(category_num[type_id-1]) + ".png")
            continue
        newIm = Image.fromarray(data, "RGBA")
        save_file_name = str(type_id) + "_"+str(category_num[type_id-1]) + ".png"
        category_num[type_id-1] += 1
        newIm.save("Boat3/" + save_file_name)
        
        boxX = np.array(boxX)
        boxY = np.array(boxY)
        boxX -= min(boxX)
        boxY -= min(boxY)
        save_dict[save_file_name] = (str(boxX[0]) +"," +str(boxY[0]) + "," +
        str(boxX[1]) +"," +str(boxY[1]) + ","+str(boxX[2]) +"," +str(boxY[2]) + ","+
        str(boxX[3]) +"," +str(boxY[3]))
with open("boat_labels.json", 'w') as json_file:
    json.dump(save_dict, json_file)
# -


[1,2,3,4] == zero_arr

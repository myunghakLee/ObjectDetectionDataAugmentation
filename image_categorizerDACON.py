import csv
from tqdm import tqdm
import shutil
import json

# +
path = "../AlphaProject/Data/"

write_dict = {}
#json_data = json.load(path + "label.json")
with open(path + "labels.json") as json_file:
    json_data = json.load(json_file)
    write_dict["features"] = []
    count = 0
    prev_im_name = ""
    for Dict in tqdm(json_data["features"]):
        im_name = Dict["properties"]['image_id']
        if im_name == prev_im_name:
            continue
        elif int(im_name.split('.')[0]) > count:
            while(int(im_name.split('.')[0]) > count):
                shutil.copy2(path+im_name, "DACON/NoneObject/"+str(count)+".png")
                count+=1
            shutil.copy2(path+im_name, "DACON/Object/"+im_name)
            count = int(im_name.split('.')[0]) +1
        else:
            shutil.copy2(path+im_name, "DACON/Object/"+im_name)
            count = int(im_name.split('.')[0]) +1
        prev_im_name = im_name


# -



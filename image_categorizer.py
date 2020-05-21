# +
import csv
from tqdm import tqdm
import shutil

im_path = "Airbus/train_v2/"
fr = open('Airbus/train_ship_segmentations_v2.csv')
fw = open('Airbus/train_ship_segmentations_v3.csv','w')
rdr = csv.reader(fr)
wtr = csv.writer(fw)
wtr.writerow(['ImageId', 'EncodedPixels'])
for i, line in tqdm(enumerate(rdr)):
    if len(line[1]) > 20:
        wtr.writerow([line[0], line[1]])
        shutil.copy2(im_path+line[0], "Airbus/Object/"+line[0])
# #        !cp {im_path+line[0]} Airbus/Object/{line[0]}
    else:
        if i == 0:
            continue
# #        !cp {im_path+line[0]} Airbus/NotObject/{line[0]}
        shutil.copy2(im_path+line[0], "Airbus/NotObject/"+line[0])

# -




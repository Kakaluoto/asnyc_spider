import os
from PIL import Image

path = r"./img"
img_list = os.listdir(path)
for i, img in enumerate(img_list):
    os.rename(os.path.join(path, img), os.path.join(path, "tuna_{}.jpg".format(i + 157)))
# for img in img_list:
#     im = Image.open(os.path.join(path, img))
#     print(img, im.getbands())

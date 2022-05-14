# coding=utf-8
import cv2
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import os
import math
from haishoku.haishoku import Haishoku


class ImageSelector:
    def __init__(self, img_path="./img"):
        self.img_path = img_path
        self.img_path_list = os.listdir(img_path)
        self.delete_list = []

    def select_function(self, img_name):
        try:
            img = cv2.imread(os.path.join(self.img_path, img_name))
            if img.shape[0] < 100 or img.shape[1] < 100:
                self.delete_list.append(img_name)
                return
            img_haishoku = Haishoku.loadHaishoku(os.path.join(self.img_path, img_name))
            color_dominant = img_haishoku.dominant
            color_hls_dominant = self.RGB2HSL(*color_dominant)
            color_hls_dominant = np.squeeze(color_hls_dominant)
            if 165 >= color_hls_dominant[0] or color_hls_dominant[0] >= 255:  # 不是蓝绿色
                self.delete_list.append(img_name)
                return
            elif color_hls_dominant[1] <= 0.25 or color_hls_dominant[2] <= 0.25:  # 是蓝绿色但是饱和度和亮度不达标
                self.delete_list.append(img_name)
                return
        except Exception as e:
            self.delete_list.append(img_name)

    def RGB2HSL(self, *args):
        BGR_point = np.array([[[args[2], args[1], args[0]]]]).astype(np.float32) / 255
        HLS_point = cv2.cvtColor(BGR_point, cv2.COLOR_BGR2HLS)
        return HLS_point

    def get_delete_list(self, max_workers=20):
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            pool.map(self.select_function, self.img_path_list)
        return self.delete_list

    def delete_image(self, path, image_list):
        for bad_image_name in image_list:
            if os.path.exists(os.path.join(path, bad_image_name)):
                os.remove(os.path.join(path, bad_image_name))
                print("Delete file '{}'".format(bad_image_name))
            else:
                print("File '{}' does not exist".format(os.path.join(path, bad_image_name)))


if __name__ == "__main__":
    path = r"./img"
    img_path_list = os.listdir(path)
    img_selector = ImageSelector(img_path=path)
    # for img_name in img_path_list:
    #     img_selector.select_function(img_name=img_name)
    delete_list = img_selector.get_delete_list(max_workers=1000)
    img_selector.delete_image(path=path, image_list=delete_list)
    # print(len(delete_list))
    # for img_name in delete_list:
    #     try:
    #         img = cv2.imread(os.path.join(path, img_name))
    #         cv2.imshow("temp", img)
    #         cv2.waitKey(200)
    #     except Exception as e:
    #         continue

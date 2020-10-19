# -*- coding:utf-8 -*-
# @author :adolf
import cv2
import numpy as np

img_path = "img0.png"
src = cv2.imread(img_path)

hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

low_hsv = np.array([100, 43, 46])
high_hsv = np.array([124, 255, 255])

mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 提取掩膜

# 黑色背景转透明部分
mask_contrary = mask.copy()
mask_contrary[mask_contrary == 0] = 1
mask_contrary[mask_contrary == 255] = 0  # 把黑色背景转白色
mask_bool = mask_contrary.astype(bool)
mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)
# 这个是把掩模图和原图进行叠加，获得原图上掩模图位置的区域
mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2BGRA)
mask_img[mask_bool] = [0, 0, 0, 0]

cv2.imwrite('label123.png', mask_img)

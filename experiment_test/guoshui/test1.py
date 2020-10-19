# -*- coding:utf-8 -*-
# @author :adolf
import cv2
import numpy as np

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')


def split_img(img):
    height, width = img.shape[:2]
    blank_r = np.ones((height, width, 3), np.uint8)
    blank_r[:] = (255, 255, 255)
    blank_y = np.ones((height, width, 3), np.uint8)
    blank_y[:] = (255, 255, 255)
    blank_b = np.ones((height, width, 3), np.uint8)
    blank_b[:] = (255, 255, 255)
    blank_black = np.ones((height, width, 3), np.uint8)
    blank_black[:] = (255, 255, 255)

    for i in range(height):
        for j in range(width):
            '''取值范围设定'''
            bgr = img[i, j]
            if bgr[0] > 210 and bgr[1] < 80 and bgr[2] < 80:  # 蓝色
                blank_b[i, j] = bgr
            if bgr[0] < 80 and bgr[1] > 210 and bgr[2] > 210:
                blank_y[i, j] = bgr
            if bgr[0] < 80 and bgr[1] < 80 and bgr[2] > 210:
                blank_r[i, j] = bgr
            if bgr[0] < 80 and bgr[1] < 80 and bgr[2] < 80:
                blank_black[i, j] = bgr
    return blank_y, blank_b, blank_r, blank_black


def pp_ocr_rec(image):
    result = ocr.ocr(image, det=False, cls=True)
    return result


if __name__ == '__main__':
    img_path = "test_img/img_1_red.png"
    img = cv2.imread(img_path)
    blank_y, blank_b, blank_r, blank_black = split_img(img)
    # cv2.imwrite("img_yellow.png", blank_y)
    # cv2.imwrite("img_blue.png", blank_b)
    # cv2.imwrite("img_red.png", blank_r)
    # cv2.imwrite("img_black.png", blank_black)

    res = pp_ocr_rec(blank_r)
    print(res)


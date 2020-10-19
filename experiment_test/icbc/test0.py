# -*- coding:utf-8 -*-
# @author :adolf
import cv2
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=False, lang="ch")
img_path = "label123.png"
img = cv2.imread(img_path)
result = ocr.ocr(img_path, cls=False, det=False)
for line in result:
    print(line)
# point = [[128.0, 0.0], [498.0, 1.0], [498.0, 37.0], [128.0, 33.0]]

# -*- coding:utf-8 -*-
# @author :adolf
import os
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')

img_path = "data/234.png"
res = ocr.ocr(img_path, det=False, cls=True)
print(res)
# img_list = os.listdir("data")
# for img_name in img_list:
#     img_path = os.path.join("data", img_name)
#     res = ocr.ocr(img_path, det=False, cls=True)
#     print("{},result:{}".format(img_name, res))

# -*- coding:utf-8 -*-
# @author :adolf
import requests
import base64
import os
from shutil import copyfile

# img_path = "/home/shizai/adolf/ocr_project/rpa_verification/experiment_test/guoshui/captcha_img/img_4666_blue.png"
img_dir = "/home/shizai/adolf/ocr_project/rpa_verification/experiment_test/guoshui/captcha_img/"
img_list = os.listdir(img_dir)
for img_name in img_list[-300:]:
    img_path = os.path.join(img_dir, img_name)
    color = img_path.split(".")[0].split("_")[-1]
    # print(color)
    with open(img_path, "rb") as f:
        b = f.read()
    # param_key: black-全黑色,red-红色,blue-蓝色,yellow-黄色
    r = requests.post("http://152.136.207.29:19812/captcha/v1", json={
        "uid": "09a253fa-11f3-11eb-b6f9-525400a21e62",
        "model_name": "TAX",
        "image": base64.b64encode(b).decode(),
        "param_key": color
    })
    print(r.json())
    res = r.json()['message']
    target_path = "/home/shizai/adolf/ocr_project/rpa_verification/experiment_test/guoshui/captcha_xy"
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    copyfile(img_path, os.path.join(target_path, res + "_" + color + ".png"))

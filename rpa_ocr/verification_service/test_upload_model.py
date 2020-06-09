# -*- coding:utf-8 -*-
# @author :adolf
import requests
import json


def get_result(encodestr):
    payload = {"image": encodestr, "type": "image"}
    r = requests.post("http://192.168.1.254:2020/upload_service/", json=payload)
    res = json.loads(r.text)
    print(res)
    return res

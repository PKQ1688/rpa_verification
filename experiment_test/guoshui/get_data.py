# -*- coding:utf-8 -*-
# @author :adolf
import base64
import numpy as np
import cv2

import requests
from invoice_captcha.utils import get_captcha_params, parse_captcha_resp, kill_captcha_fast, ua

CAPTCHA_URL = "https://fpcy.guangdong.chinatax.gov.cn/NWebQuery/yzmQuery"

# 发票代码
key1 = "011111111111"
# 发票号码
key2 = "11111111"


# # 开票日期
# key3 = "20200603"
# # 校验码或发票金额
# key4 = "000000"

def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image


def fetch_captcha(invoice_code, invoice_no):
    sess = requests.Session()

    # 使用代理，需要自备代理
    # sess.proxies = proxy
    sess.headers = {"User-Agent": ua.random}

    # 获取验证码请求参数
    payload = get_captcha_params(
        invoice_code=invoice_code, invoice_no=invoice_no
    )

    # 通过官网获取验证码
    r = sess.get(CAPTCHA_URL, params=payload)

    # 验证码请求参数解密
    plain_dict = parse_captcha_resp(r)

    # 验证码请求返回明文
    # key1 图片base64
    # key4 验证码需要识别的颜色代码
    # print("解密参数 --- ", plain_dict)
    return plain_dict['key1'], plain_dict['key4']
    # 调用识别测试接口
    # captcha_text = kill_captcha_fast(
    #     plain_dict,
    #     # 默认API有使用次数限制，可联系作者QQ：27009583，测试独立接口
    #     # api="http://kerlomz-ac86u.asuscomm.com:19811/captcha/v1"
    # )
    #
    # # 输出识别结果
    # print("识别结果 --- ", captcha_text)


CAPTCHA_TYPE = {
    "00": "black",
    "01": "red",
    "02": "yellow",
    "03": "blue"
}
if __name__ == '__main__':
    import os

    # for i in range(1):
    #     fetch_captcha(key1, key2)
    for i in range(10000):
        img_base, color = fetch_captcha(key1, key2)
        image = base64_cv2(img_base)
        if not os.path.exists("captcha_img"):
            os.mkdir("captcha_img")
        cv2.imwrite("captcha_img/img_{}_{}.png".format(str(i), CAPTCHA_TYPE[color]), image)

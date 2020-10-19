import os
import random
from fake_captcha.ImageCaptcha import ImageCaptcha
import string

with open("data/chars.txt", "r", encoding="utf-8") as f:
    captcha_cn = f.read()  # 中文字符集

captcha_en = string.digits + string.ascii_lowercase  # 英文字符集

color_dict = ["黑", "黄", "蓝", "红"]


def random_captcha_text(num):

    # 选择0-2个英文字母（英文字母种类较少，不需要太多，可根据需求自行设置）
    en_num = random.randint(0, 2)
    cn_num = num - en_num

    example_en = random.sample(captcha_en, en_num)
    example_cn = random.sample(captcha_cn, cn_num)
    example = example_cn + example_en
    random.shuffle(example)

    # 将列表里的片段变为字符串并返回
    verification_code = ''.join(example)
    return verification_code


# 生成字符对应的验证码
def generate_captcha_image(path="fake_pic_1", num=1):

    imc = ImageCaptcha(width=90, height=35, fonts=[r"actionj.ttf", r"simsun.ttc"], font_sizes=(18, 19),
                       text_colors=["black", "yellow", "blue", "red"])

    # 获得随机生成的6个验证码字符
    captcha_text = random_captcha_text(6)

    if not os.path.exists(path):
        print("目录不存在!,已自动创建")
        os.makedirs(path)
    for _ in range(num):
        image, colors = imc.generate_image(captcha_text)
        colors = "".join([color_dict[int(c)] for c in colors])
        print("生成的验证码的图片为：", captcha_text + "_" + colors)
        image.save(os.path.join(path, captcha_text + "_" + colors) + '.png')


if __name__ == '__main__':
    for _ in range(1000000):
        generate_captcha_image(num=1)



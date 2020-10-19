# -*- coding:utf-8 -*-
# @author :adolf
import skimage.metrics
import cv2

import matplotlib.pyplot as plt


im1_path = "fake_pic_1/惰临垃馆li_黑红黄蓝黄黑.png"
im2_path = "../captcha_img/img_4051_red.png"
im1 = cv2.imread(im1_path)
im2 = cv2.imread(im2_path)
plt.imshow(im1)
plt.title("fake")
plt.show()

plt.imshow(im2)
plt.title('get')
plt.show()

# im1 = cv2.imread(im1_path, cv2.IMREAD_GRAYSCALE)
# im2 = cv2.imread(im2_path, cv2.IMREAD_GRAYSCALE)
psnr = skimage.metrics.peak_signal_noise_ratio(im1, im2)
ssim = skimage.metrics.structural_similarity(im1, im2, multichannel=True)
print(psnr)
print(ssim)

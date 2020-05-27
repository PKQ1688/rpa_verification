# -*- coding:utf-8 -*-
# @author :adolf
import cv2
import torch.utils.data as data
import torch
import torchvision.transforms as transforms


class rawdataset(data.Dataset):
    def __init__(self, file_path, data_list, alphabet_dict=None):
        all_data_list = list()
        for png_name in data_list:
            img = cv2.imread(file_path + png_name)
            assert img.shape[2] == 3, "请读入3通道图片"
            img = cv2.resize(img, (74, 32))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            label = png_name.split('.')[0]
            all_data_list.append((img, label))
        self.img_input = all_data_list

        self.alphabet_dict = alphabet_dict
        self.transform = transforms.Compose([transforms.ToTensor()])
        self.target_transform = self.converter_text_to_label

    def __len__(self):
        return len(self.img_input)

    def __getitem__(self, index):
        img, label = self.img_input[index]
        img = self.transform(img)
        label, length = self.target_transform(label)
        return img, label, length

    def converter_text_to_label(self, label_str):
        label = [self.alphabet_dict[char] for char in label_str]
        length = [len(label)]
        return (torch.IntTensor(label), torch.IntTensor(length))

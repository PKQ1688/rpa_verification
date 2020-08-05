# -*- coding:utf-8 -*-
# @author :adolf
import torch
import torch.nn as nn


class BidirectionalLSTM(nn.Module):

    def __init__(self, nIn, nHidden, nOut):
        super(BidirectionalLSTM, self).__init__()

        self.rnn = nn.LSTM(nIn, nHidden, bidirectional=True)
        self.embedding = nn.Linear(nHidden * 2, nOut)

    def forward(self, input):
        recurrent, _ = self.rnn(input)
        T, b, h = recurrent.size()
        t_rec = recurrent.view(T * b, h)

        output = self.embedding(t_rec)
        output = output.view(T, b, -1)

        return output


class CRNN(nn.Module):

    def __init__(self, imgH, nc, nclass, nh, n_rnn=2, leakyRelu=False, debug=False):
        super(CRNN, self).__init__()

        self.debug = debug
        assert imgH % 16 == 0, 'imgH has to be a multiple of 16'

        multi = (imgH / 16) - 1
        multi_channel = int(512 * multi)

        ks = [3, 3, 3, 3, 3, 3, 2]
        ps = [1, 1, 1, 1, 1, 1, 0]
        ss = [1, 1, 1, 1, 1, 1, 1]
        nm = [64, 128, 256, 256, 512, 512, 512, 512, 512, 1024]

        cnn = nn.Sequential()

        def convRelu(i, batchNormalization=False):
            nIn = nc if i == 0 else nm[i - 1]
            nOut = nm[i]
            cnn.add_module('conv{0}'.format(i),
                           nn.Conv2d(nIn, nOut, ks[i], ss[i], ps[i]))
            if batchNormalization:
                cnn.add_module('batchnorm{0}'.format(i), nn.BatchNorm2d(nOut))
            if leakyRelu:
                cnn.add_module('relu{0}'.format(i),
                               nn.LeakyReLU(0.2, inplace=True))
            else:
                cnn.add_module('relu{0}'.format(i), nn.ReLU(True))

        convRelu(0)
        cnn.add_module('pooling{0}'.format(0), nn.MaxPool2d(2, 2))  # 64x16x64
        convRelu(1)
        cnn.add_module('pooling{0}'.format(1), nn.MaxPool2d(2, 2))  # 128x8x32
        convRelu(2, True)
        convRelu(3)
        cnn.add_module('pooling{0}'.format(2),
                       nn.MaxPool2d((2, 2), (2, 1), (0, 1)))  # 256x4x16
        convRelu(4, True)
        convRelu(5)
        cnn.add_module('pooling{0}'.format(3),
                       nn.MaxPool2d((2, 2), (2, 1), (0, 1)))  # 512x2x16

        convRelu(6, True)  # 512x1x16

        # if debug:
        # convRelu(1, True)
        # cnn.add_module('pooling{0}'.format(4),
        #                nn.AvgPool2d((3, 1), (1, 1)))

        self.cnn = cnn
        self.rnn = nn.Sequential(
            BidirectionalLSTM(multi_channel, nh, nh),
            BidirectionalLSTM(nh, nh, nclass))

    def forward(self, input):
        # conv features
        conv = self.cnn(input)

        # if self.debug:
        # conv = torch.reshape(conv, (b, c, h * w))
        # for i in range()
        # conv1 = conv[:, :, 0, :]
        # conv2 = conv[:, :, 1, :]
        # conv = torch.stack((conv1, conv2), 1)
        # conv = torch.reshape(conv, (b, h * c, w))
        # print(conv.size())
        # conv = torch.flatten(conv, start_dim=1, end_dim=2).unsqueeze(dim=2)
        # print(conv.size())

        b, c, h, w = conv.size()
        conv = conv.view(b, c * h, w).unsqueeze(dim=2)

        b, c, h, w = conv.size()
        # print('1111', conv.size())
        # print(b, c, h, w)
        assert h == 1  # , "the height of conv must be 1"
        conv = conv.squeeze(2)
        conv = conv.permute(2, 0, 1)  # [w, b, c]

        # rnn features
        output = self.rnn(conv)
        return output

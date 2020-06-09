# -*- coding:utf-8 -*-
# @author :adolf
from torch import nn
import torch.onnx


def convert_model(torch_model, model_path):
    torch_model.load_state_dict(torch.load(model_path, map_location="cpu"))
    torch_model.eval()
    batch_size = 1
    x = torch.randn(batch_size, 1, 224, 224, requires_grad=True)
    # torch_out = torch_model(x)

    torch.onnx.export(torch_model,  # model being run
                      x,  # model input (or a tuple for multiple inputs)
                      "super_resolution.onnx",  # where to save the model (can be a file or file-like object)
                      export_params=True,  # store the trained parameter weights inside the model file
                      opset_version=10,  # the ONNX version to export the model to
                      do_constant_folding=True,  # wether to execute constant folding for optimization
                      input_names=['input'],  # the model's input names
                      output_names=['output'],  # the model's output names
                      dynamic_axes={'input': {0: 'batch_size'},  # variable lenght axes
                                    'output': {0: 'batch_size'}})

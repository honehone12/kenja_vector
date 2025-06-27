import os
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoProcessor
from PIL import Image

__device = None
__model = None
__processor = None

def init_siglip_model():
    global __device
    global __model
    global __processor

    model_name = os.getenv('SIGLIP_MODEL')
    if model_name is None:
        raise ValueError('env for siglip model is not set')
    
    __device = torch.device('cuda')
    __model = AutoModel.from_pretrained(model_name).eval().to(__device)
    __processor = AutoProcessor.from_pretrained(model_name, use_fast=True)

def image_vector(path: str):
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')
    if __device is None:
        raise ValueError('device is not initialized')

    img = Image.open(path).convert('RGB')
    with torch.no_grad():
        input = __processor(images=[img], return_tensors='pt').to(__device)
        raw = __model.get_image_features(**input)
        return F.normalize(raw, p=2.0, dim=-1).squeeze(0)

import os
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
import torch
import torch.nn.functional as F

__model = None
__processor = None
__device = None

def init_clip_model():
    global __model
    global __processor
    global __device

    model_name = os.getenv('CLIP_MODEL')
    if model_name is None:
        raise ValueError('env for clip model is not set')

    __device = torch.device('cuda')

    __model = CLIPModel.from_pretrained(model_name).eval().to(__device)

    __processor = CLIPProcessor.from_pretrained(model_name)

def image_vector(path: str):
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')
    if __device is None:
        raise ValueError('device is not initialized')

    img = Image.open(path)
    with torch.no_grad():
        input = __processor(images=img, return_tensors='pt')
        input = {k: v.to(__device) for k, v in input.items()}
        v = __model.get_image_features(**input)
        return F.normalize(v, p=2.0, dim=-1).squeeze(0)

import os
from transformers import AutoModel, AutoImageProcessor
import torch
import torch.nn.functional as F
from PIL import Image

__processor = None
__model = None
__device = None

def init_image_tsfm_model():
    global __processor
    global __model
    global __device

    model_name = os.getenv('IMG_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for image embed model is not set')

    __device = torch.device('cuda')
    __processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
    __model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    __model.to(__device)
    __model.eval()

def image_vector(img_path: str):
    if __processor is None:
        raise ValueError('processor is not initialized')
    if __model is None:
        raise ValueError('model is not initialized')
    if __device is None:
        raise ValueError('device is not initialized')

    with torch.no_grad():
        img = Image.open(img_path)
        proc = __processor(img, return_tensors='pt', device='cuda')
        raw = __model(**proc).last_hidden_state
        crs_tkn = raw[:, 0]
        return F.normalize(crs_tkn, p=2.0, dim=1).squeeze(0)

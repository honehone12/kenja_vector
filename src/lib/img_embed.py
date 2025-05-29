import os
from transformers import AutoModel, AutoImageProcessor
import torch
import torch.nn.functional as F
from numpy import ndarray
from PIL import Image

__processor = None
__model = None

def init_img_model():
    global __processor
    global __model

    model_name = os.getenv('IMG_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for IMG_EMBED_MODEL is not set')

    __processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
    __model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    __model.eval()

def img_vector(img_path: str) -> ndarray:
    if __processor is None:
        raise ValueError('processor is not initialized')
    if __model is None:
        raise ValueError('model is not initialized')

    with torch.no_grad():
        img = Image.open(img_path)
        proc = __processor(img, return_tensors='pt')
        raw = __model(**proc).last_hidden_state
        crs_tkn = raw[:, 0]
        normalized = F.normalize(crs_tkn, p=2, dim=1) 
        return normalized.squeeze().numpy()

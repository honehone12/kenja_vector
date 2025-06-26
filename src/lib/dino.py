import os
from PIL import Image
from transformers import AutoModel, AutoImageProcessor
import torch
import torch.nn.functional as F

__model = None
__processor = None
__device = None

def init_dino_model():
    global __model
    global __processor
    global __device

    model_name = os.getenv('IMG_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for image embed model is not set')
    
    __device = torch.device('cuda')

    __model = AutoModel.from_pretrained(
        model_name,
        trust_remote_code=True
    ).eval().to(__device)

    __processor = AutoImageProcessor.from_pretrained(model_name)

def image_vector(path: str):
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')
    if __device is None:
        raise ValueError('device is not initialized')

    img = Image.open(path)
    input = __processor(
        images=img, 
        return_tensors="pt"
    )
    input = {k: v.to(__device) for k, v in input.items()}
    raw = __model(**input).last_hidden_state
    crs_tkn = raw[:, 0]
    return F.normalize(crs_tkn, p=2.0, dim=-1).squeeze(0)

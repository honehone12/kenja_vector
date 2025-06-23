import os
import torch
import torch.nn.functional as F
from PIL import Image
from colpali_engine.models import ColQwen2_5, ColQwen2_5_Processor

__model = None
__processor = None

def init_multi_modal_model():
    global __model
    global __processor

    model_name = os.getenv('MULTI_MODAL_MODEL')
    if model_name is None:
        raise ValueError('env for mult modal model is not set')

    __model = ColQwen2_5.from_pretrained(
        model_name,
        device_map='cuda:0',
        torch_dtype=torch.bfloat16,
        attn_implementation='sdpa'
    ).eval()

    __processor = ColQwen2_5_Processor.from_pretrained(model_name, use_fast=True)

def txt_vector(sentence: str) -> torch.Tensor:
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')

    with torch.no_grad():
        input = __processor.process_queries([sentence]).to(__model.device)
        txt_embed = __model(**input)
        return F.normalize(txt_embed[0], p=2.0, dim=-1)

def img_vector(path: str) -> torch.Tensor:
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')

    with torch.no_grad():
        img = Image.open(path)
        input = __processor.process_images([img]).to(__model.device)
        img_embed = __model(**input)
        return F.normalize(img_embed[0], p=2.0, dim=-1)
        
import os
import torch
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
        device_map='cuda:0'
    ).eval()

    __processor = ColQwen2_5_Processor.from_pretrained(
        model_name,
        device_map='cuda:0'
    )

def txt_vector(sentence: str):
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')

    input = __processor.process_queries([sentence]).to(__model.device)
    
    with torch.no_grad():
        txt_embed = __model(**input)
        return txt_embed

def img_vector(path: str):
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')

    img = Image.open(path)
    input = __processor.process_images([img]).to(__model.device)
    
    with torch.no_grad():
        img_embed = __model(**input)
        return img_embed
        
import os
import torch
import torch.nn.functional as F
from PIL import Image
from colpali_engine.models import ColQwen2 as Model, ColQwen2Processor as Processor
#from colpali_engine.models import ColPali as Model, ColPaliProcessor as Processor

__model = None
__processor = None

def init_multi_modal_model():
    global __model
    global __processor

    model_name = os.getenv('MULTI_MODAL_MODEL')
    if model_name is None:
        raise ValueError('env for mult modal model is not set')

    __model = Model.from_pretrained(
        model_name,
        device_map='cuda:0',
        torch_dtype=torch.bfloat16
    ).eval()

    __processor = Processor.from_pretrained(
        model_name,
        device_map='cuda:0', 
        use_fast=True
    )

def txt_vector(sentence: str) -> torch.Tensor:
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')

    with torch.no_grad():
        input = __processor.process_queries([sentence]).to(__model.device)
        embed = __model(**input)
        return post_process(embed[0])

def img_vector(path: str) -> torch.Tensor:
    if __model is None:
        raise ValueError('model is not initialized')
    if __processor is None:
        raise ValueError('processor is not initialized')

    with torch.no_grad():
        img = Image.open(path)
        input = __processor.process_images([img]).to(__model.device)
        embed = __model(**input)
        return post_process(embed[0])
        
        
def post_process(v: torch.Tensor) -> torch.Tensor:
    normalized = F.normalize(v, p=2.0, dim=-1)
    return torch.mean(normalized, dim=0)

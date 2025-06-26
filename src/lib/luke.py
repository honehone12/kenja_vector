import os
from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F

__model = None
__tokenizer = None
__device = None

def init_luke_model():
    global __model
    global __tokenizer
    global __device

    model_name = os.getenv('NAME_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for name embed model is not set')

    __device = torch.device('cuda')

    __model = AutoModel.from_pretrained(
        model_name,
        trust_remote_code=True
    ).eval().to(__device)

    __tokenizer = AutoTokenizer.from_pretrained(model_name)

def name_vector(text: str):
    if __model is None:
        raise ValueError('model is not initialized')
    if __tokenizer is None:
        raise ValueError('tokenizer is not initialized')
    if __device is None:
        raise ValueError('device is not initialized')

    input = __tokenizer(
        text, 
        return_tensors='pt', 
        truncation=True
    )
    input = {k: v.to(__device) for k, v in input.items()}
    raw = __model(**input).last_hidden_state
    cls_tkn = raw[:, 0, :]
    return F.normalize(cls_tkn, p=2.0, dim=-1).squeeze(0)
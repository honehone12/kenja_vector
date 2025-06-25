import os
import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

__PROMPT = 'passage'
__PREFIX = 'search_document: '

__model = None

def init_sentence_tsfm_model():
    global __model

    model_name = os.getenv('TXT_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for text embed model is not set')

    __model = SentenceTransformer(
        model_name, 
        device='cuda',
        trust_remote_code=True
    )

def sentence_vector(sentence: str):
    if __model is None:
        raise ValueError('model is not initialized')

    raw = __model.encode(
        __PREFIX + sentence, 
        show_progress_bar=False,
        convert_to_tensor=True
    )
    return post_process(raw)
    

def sentence_vector_v2(sentence: str):
    if __model is None:
        raise ValueError('model is not initialized')

    raw = __model.encode(
        sentence, 
        prompt_name=__PROMPT,
        show_progress_bar=False,
        convert_to_tensor=True
    )
    return post_process(raw)

def post_process(v: torch.Tensor):
    return F.normalize(v, p=2.0, dim=-1)

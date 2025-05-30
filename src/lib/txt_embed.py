import os
from typing import Any
from sentence_transformers import SentenceTransformer
from numpy import ndarray
from numpy.linalg import norm

__PROMPT = 'passage'
__PREFIX = 'search_document: '

__model = None

def init_txt_model():
    global __model

    model_name = os.getenv('TXT_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for TEXT_EMBED_MODEL is not set')

    __model = SentenceTransformer(model_name, trust_remote_code=True)

def normalize(raw: ndarray[Any, Any]):
    normal = norm(raw)
    if normal == 0:
        return raw
    else:
        return raw / normal

def txt_vector(sentence: str):
    if __model is None:
        raise ValueError('model is not initialized')

    raw = __model.encode(
        __PREFIX + sentence, 
        show_progress_bar=False,
        convert_to_numpy=True
    )
    return normalize(raw)
    

def txt_vector_v2(sentence: str):
    if __model is None:
        raise ValueError('model is not initialized')

    raw = __model.encode(
        sentence, 
        prompt_name=__PROMPT,
        show_progress_bar=False,
        convert_to_numpy=True
    )
    return normalize(raw)

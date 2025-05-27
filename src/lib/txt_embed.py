import os
from sentence_transformers import SentenceTransformer
from torch import Tensor

__PROMPT = 'passage'

__model = None

def init_model():
    global __model

    model_name = os.getenv('TXT_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for TEXT_EMBED_MODEL is not set')

    __model = SentenceTransformer(model_name, trust_remote_code=True)

def txt_vector(sentence: str) -> Tensor:
    if __model is None:
        raise ValueError('model is not initialized')

    return __model.encode(
        sentence, 
        prompt_name=__PROMPT,
        normalize_embeddings=True
    )

import os
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import normalize_embeddings
from numpy import ndarray
from numpy.linalg import norm

__PROMPT = 'passage'

__model = None

def init_txt_model():
    global __model

    model_name = os.getenv('TXT_EMBED_MODEL')
    if model_name is None:
        raise ValueError('env for TEXT_EMBED_MODEL is not set')

    __model = SentenceTransformer(model_name, trust_remote_code=True)

def txt_vector(sentence: str) -> ndarray:
    if __model is None:
        raise ValueError('model is not initialized')

    raw = __model.encode(
        sentence, 
        prompt_name=__PROMPT,
        show_progress_bar=False,
        convert_to_numpy=True
    )
    normal = norm(raw)
    if normal == 0:
        return raw
    else:
        return raw / normal


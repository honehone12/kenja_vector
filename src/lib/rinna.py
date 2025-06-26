import os
from PIL import Image
import torch
import torch.nn.functional as F
import japanese_clip as ja_clip

__preprocessor = None
__model = None
__device = None

def init_rinna_model():
    model_name = os.getenv('CLIP_MODEL')
    if model_name is None:
        raise ValueError('env for clip model name is not set')
    cache_dir = os.getenv('JP_CACHE')
    if cache_dir is None:
        raise ValueError('env for jp cache dir is not set')

    __device = 'cuda'
    __model, __preprocessor = ja_clip.load(
        model_name,
        cache_dir=cache_dir,
        device=__device
    )

def image_vector(path: str):
    if __model is None:
        raise ValueError('model is not initialized')
    if __preprocessor is None:
        raise ValueError('processor is not initialized')
    if __device is None:
        raise ValueError('device is not initialized')

    img = Image.open(path)
    with torch.no_grad():
        input = __preprocessor(img).unsqueeze(0).to(__device)
        raw = __model.get_image_features(input)
        return F.normalize(raw, p=2.0, dim=-1)

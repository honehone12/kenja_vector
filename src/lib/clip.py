import os
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

__model = None
__processor = None

def init_clip_model():
    global __model
    global __processor

    model_name = os.getenv('CLIP_MODEl')
    __model = CLIPModel.from_pretrained(
        model_name,
        device_map='cuda'
    ).eval()

    __processor = CLIPProcessor.from_pretrained(
        model_name,
        device_map='cuda',
        use_fase=True
    )

def sentence_vector(sentence: str):
    if __model is None:
        raise ValueError('model is not initialize')
    if __processor is None:
        raise ValueError('processor is not initialized')

    input = __processor(text=[sentence])
    v = __model.encode_text(input)
    return v

def image_vector(path: str):
    if __model is None:
        raise ValueError('model is not initialize')
    if __processor is None:
        raise ValueError('processor is not initialized')

    img = Image.open(path)
    input = __processor(images=[img])
    v = __model.encode_text(input)
    return v
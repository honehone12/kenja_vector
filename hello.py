from sentence_transformers import SentenceTransformer

model = SentenceTransformer('nomic-ai/nomic-embed-text-v2-moe', trust_remote_code=True)
# model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
sentences = [
    'Select your preferences and run the install command. Stable represents the most currently tested and supported version of PyTorch. This should be suitable for many users. Preview is available if you want the latest, not fully tested and supported, builds that are generated nightly. Please ensure that you have met the prerequisites below (e.g., numpy), depending on your package manager. You can also install previous versions of PyTorch. Note that LibTorch is only available for C++. ',
    'PyTorch can be installed and used on various Linux distributions. Depending on your system and compute requirements, your experience with PyTorch on Linux may vary in terms of processing time. It is recommended, but not required, that your Linux system has an NVIDIA or AMD GPU in order to harness the full power of PyTorch’s CUDA support or ROCm support.'
]
#embeddings = model.encode(sentences, 'passage')
embeddings = model.encode(sentences)
print('shape of encoded vector ', embeddings.shape)
similarity = model.similarity(embeddings[0], embeddings[1])
print(f'similarity = {similarity}')

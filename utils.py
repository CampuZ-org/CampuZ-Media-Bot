from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def compute_vector(text: str) -> bytes:
    """Вычисляет семантический вектор текста."""
    return model.encode(text).tobytes()

def compare_vectors(vector1: bytes, vector2: bytes) -> float:
    """Сравнивает два вектора по косинусному расстоянию."""
    v1 = model.decode(vector1)
    v2 = model.decode(vector2)
    return util.cos_sim(v1, v2).item()
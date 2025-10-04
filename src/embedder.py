# src/embedder.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



def embed_texts(texts,model):
    embeddings = [model.encode(text, show_progress_bar=False, convert_to_numpy=True) for text in texts]
    return embeddings

def cos_sim(query,texts) :
    res = []
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embed = model.encode(query, show_progress_bar=False, convert_to_numpy=True)
    embeddings = embed_texts(texts,model)
    for i in range (len(embeddings)):
        res_embed = cosine_similarity([query_embed], [embeddings[i]])
        res.append((texts[i], res_embed[0][0]))    
    
    res = [res_item for res_item in res if res_item[1] > 0.2]
    return res


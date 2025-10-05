import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def embed_texts(texts):
    if OPENAI_KEY:
        import openai
        openai.api_key = OPENAI_KEY
        resp = openai.Embeddings.create(model='text-embedding-3-small', input=texts)
        return [r['embedding'] for r in resp['data']]
    else:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        vectors = model.encode(texts, show_progress_bar=False)
        return vectors.tolist()

if __name__ == '__main__':
    print('embedding test...')
    v = embed_texts(["Apple announces new iPhone", "Earnings beat for company X"])
    print(len(v), len(v[0]))

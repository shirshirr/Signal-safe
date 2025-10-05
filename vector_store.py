import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV', 'us-west1-gcp')
PINECONE_INDEX = os.getenv('PINECONE_INDEX', 'signalsafe-index')

class InMemoryVectorStore:
    def __init__(self):
        self.ids, self.vectors, self.metadata = [], [], []
    def upsert(self, ids, vectors, metadata_list=None):
        for _id, vec, meta in zip(ids, vectors, metadata_list or [{}]*len(ids)):
            self.ids.append(_id)
            self.vectors.append(np.array(vec, dtype=float))
            self.metadata.append(meta or {})
    def query(self, vector, top_k=5, include_metadata=True):
        if not self.vectors: return []
        q = np.array(vector, dtype=float)
        mat = np.stack(self.vectors)
        sims = (mat @ q) / (np.linalg.norm(mat,axis=1)*np.linalg.norm(q)+1e-12)
        idxs = np.argsort(-sims)[:top_k]
        return [{'id': self.ids[i], 'score': float(sims[i]), 'metadata': self.metadata[i]} for i in idxs]

class VectorStore:
    def __init__(self, dimension=1536):
        self._use_pinecone = False
        try:
            import pinecone
            if PINECONE_API_KEY:
                pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
                if PINECONE_INDEX not in pinecone.list_indexes():
                    pinecone.create_index(PINECONE_INDEX, dimension=dimension)
                self._index = pinecone.Index(PINECONE_INDEX)
                self._use_pinecone = True
            else:
                self._index = InMemoryVectorStore()
        except Exception:
            self._index = InMemoryVectorStore()
    def upsert(self, ids, vectors, metadata_list=None):
        if self._use_pinecone:
            to_upsert = [(_id, vec, meta) for _id, vec, meta in zip(ids, vectors, metadata_list or [{}]*len(ids))]
            self._index.upsert(vectors=to_upsert)
        else:
            self._index.upsert(ids, vectors, metadata_list)
    def query(self, vector, top_k=5, include_metadata=True):
        if self._use_pinecone:
            resp = self._index.query(vector=vector, top_k=top_k, include_metadata=include_metadata)
            return resp.get('matches', [])
        else:
            return self._index.query(vector, top_k=top_k, include_metadata=include_metadata)

if __name__ == '__main__':
    print('vector store: using in-memory fallback')

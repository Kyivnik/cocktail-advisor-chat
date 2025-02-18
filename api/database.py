import os
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Initialize the embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Path to the dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/cocktails.csv")

class CocktailDatabase:
    def __init__(self):
        # Load data
        self.df = pd.read_csv(DATA_PATH)
        # Create a text representation for each cocktail
        self.texts = self.df.apply(
            lambda row: f"{row['name']} | {row['ingredients']} | {row.get('instructions', '')}", axis=1
        ).tolist()
        # Compute embeddings for each cocktail
        self.embeddings = embedding_model.encode(self.texts, convert_to_numpy=True)
        self.dimension = self.embeddings.shape[1]
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings)

    def search(self, query: str, k: int = 5):
        query_embedding = embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for idx in indices[0]:
            if idx < len(self.df):
                results.append(self.df.iloc[idx].to_dict())
        return results

class MemoryDatabase:
    """
    A simple in-memory database to store user preferences.
    Each preference is stored as text along with its embedding.
    """
    def __init__(self):
        self.memories = []  # List of memory texts (e.g., "rum, lime, mint")
        self.embeddings = None
        self.dimension = embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)

    def add_memory(self, memory_text: str):
        self.memories.append(memory_text)
        new_embedding = embedding_model.encode([memory_text], convert_to_numpy=True)
        if self.embeddings is None:
            self.embeddings = new_embedding
        else:
            self.embeddings = np.vstack([self.embeddings, new_embedding])
        self.index.reset()  # Rebuild the index with updated embeddings
        self.index.add(self.embeddings)

    def search(self, query: str, k: int = 5):
        if self.embeddings is None or len(self.memories) == 0:
            return []
        query_embedding = embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for idx in indices[0]:
            if idx < len(self.memories):
                results.append(self.memories[idx])
        return results

# Global instances
cocktail_db = CocktailDatabase()
memory_db = MemoryDatabase()
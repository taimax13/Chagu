from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the EmbeddingGenerator class.

        :param model_name: The name of the Sentence Transformer model to use (default: all-MiniLM-L6-v2).
        """
        self.model = SentenceTransformer(model_name)
        print(f"Loaded embedding model: {model_name}")

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generates an embedding for a given text.

        :param text: The input text to be embedded.
        :return: The embedding as a numpy array.
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return np.array([])

    def batch_generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generates embeddings for a batch of texts.

        :param texts: A list of texts to be embedded.
        :return: A list of embeddings as numpy arrays.
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            print(f"Error generating batch embeddings: {str(e)}")
            return []

    def compute_similarity(self, query_embedding: np.ndarray, document_embeddings: List[np.ndarray]) -> List[float]:
        """
        Computes cosine similarity between a query embedding and a list of document embeddings.

        :param query_embedding: The embedding of the query.
        :param document_embeddings: A list of embeddings for documents.
        :return: A list of similarity scores.
        """
        try:
            similarities = cosine_similarity([query_embedding], document_embeddings)[0]
            return similarities.tolist()
        except Exception as e:
            print(f"Error computing similarity: {str(e)}")
            return []

    def find_most_similar(self, query: str, documents: List[str], top_k: int = 5) -> List[Dict]:
        """
        Finds the most similar documents to a given query.

        :param query: The input query text.
        :param documents: A list of document texts.
        :param top_k: The number of most similar documents to return.
        :return: A list of dictionaries with 'document' and 'similarity' keys.
        """
        query_embedding = self.generate_embedding(query)
        document_embeddings = self.batch_generate_embeddings(documents)

        # Check if embeddings are valid
        if query_embedding is None or query_embedding.size == 0 or len(document_embeddings) == 0:
            print("Error: Invalid embeddings. Please check the input data.")
            return []

        similarities = self.compute_similarity(query_embedding, document_embeddings)
        ranked_results = sorted(
            [{"document": doc, "similarity": sim} for doc, sim in zip(documents, similarities)],
            key=lambda x: x["similarity"],
            reverse=True
        )
        return ranked_results[:top_k]


if __name__ == "__main__":
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "The sky is blue and the sun is shining.",
        "Machine learning models can be used for document search.",
        "Chagu protocol enhances data security using blockchain.",
        "Hugging Face offers a variety of NLP models."
    ]
    query = "What can be used for document search?"

    embedding_generator = EmbeddingGenerator()
    most_similar_docs = embedding_generator.find_most_similar(query, documents, top_k=3)

    print("Most Similar Documents:")
    for result in most_similar_docs:
        print(f"Document: {result['document']}, Similarity: {result['similarity']:.4f}")

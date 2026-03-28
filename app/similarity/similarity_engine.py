from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:
    def build_similarity_matrix(self, vectors):
        return cosine_similarity(vectors)
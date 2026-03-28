class StatisticalBaseline:
    def __init__(
        self,
        similarity_threshold: float = 0.05,
        min_neighbors: int = 1,
    ) -> None:
        self.similarity_threshold = similarity_threshold
        self.min_neighbors = min_neighbors

    def analyze(self, similarity_matrix) -> list[dict]:
        results = []

        for i in range(len(similarity_matrix)):
            similarities = []

            for j in range(len(similarity_matrix[i])):
                if i == j:
                    continue
                similarities.append(float(similarity_matrix[i][j]))

            similar_neighbors = sum(
                1 for score in similarities if score >= self.similarity_threshold
            )
            max_similarity = max(similarities) if similarities else 0.0
            avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0

            suspicion_score = (0.7 * max_similarity) + (0.3 * avg_similarity)
            label = 1 if similar_neighbors >= self.min_neighbors else 0

            results.append(
                {
                    "label": label,
                    "similar_neighbors": similar_neighbors,
                    "max_similarity": round(max_similarity, 3),
                    "avg_similarity": round(avg_similarity, 3),
                    "suspicion_score": round(suspicion_score, 3),
                }
            )

        return results

    def predict(self, similarity_matrix) -> list[int]:
        return [item["label"] for item in self.analyze(similarity_matrix)]
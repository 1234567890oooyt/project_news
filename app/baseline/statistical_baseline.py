class StatisticalBaseline:
    def __init__(self, similarity_threshold: float = 0.3, min_neighbors: int = 1) -> None:
        self.similarity_threshold = similarity_threshold
        self.min_neighbors = min_neighbors

    def predict(self, similarity_matrix) -> list[int]:
        predictions = []

        for i in range(len(similarity_matrix)):
            similar_count = 0

            for j in range(len(similarity_matrix[i])):
                if i == j:
                    continue

                if similarity_matrix[i][j] >= self.similarity_threshold:
                    similar_count += 1

            label = 1 if similar_count >= self.min_neighbors else 0
            predictions.append(label)

        return predictions
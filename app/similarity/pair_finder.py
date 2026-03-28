class SimilarPairFinder:
    def find_pairs(self, messages: list, similarity_matrix, threshold: float = 0.05) -> list[dict]:
        pairs = []

        for i in range(len(messages)):
            for j in range(i + 1, len(messages)):
                score = float(similarity_matrix[i][j])

                if score >= threshold:
                    pairs.append(
                        {
                            "message_1": messages[i],
                            "message_2": messages[j],
                            "score": score,
                        }
                    )

        pairs.sort(key=lambda x: x["score"], reverse=True)
        return pairs
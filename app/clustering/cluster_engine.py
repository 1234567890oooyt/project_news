from sklearn.cluster import DBSCAN
import numpy as np


class ClusterEngine:
    def cluster(self, similarity_matrix, eps: float = 0.8, min_samples: int = 2) -> list[int]:
        distance_matrix = 1 - similarity_matrix
        distance_matrix = np.clip(distance_matrix, 0, 1)

        model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric="precomputed"
        )

        labels = model.fit_predict(distance_matrix)
        return labels.tolist()
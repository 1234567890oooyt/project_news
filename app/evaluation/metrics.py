from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


class MetricsEvaluator:
    def evaluate(self, y_true: list[int], y_pred: list[int]) -> dict:
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1_score": f1_score(y_true, y_pred, zero_division=0),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        }
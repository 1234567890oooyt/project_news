from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfFeatureExtractor:
    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, texts: list[str]):
        return self.vectorizer.fit_transform(texts)
from app.collectors.news_collector import NewsCollector
from app.collectors.telegram_collector import TelegramCollector
from app.preprocessing.cleaner import TextCleaner
from app.storage.db import SessionLocal, init_db
from app.storage.models import Message
from app.features.tfidf_vectorizer import TfidfFeatureExtractor
from app.similarity.similarity_engine import SimilarityEngine
from app.similarity.pair_finder import SimilarPairFinder
from app.baseline.statistical_baseline import StatisticalBaseline
from app.clustering.cluster_engine import ClusterEngine


def save_messages(messages: list[dict]) -> None:
    session = SessionLocal()
    cleaner = TextCleaner()

    try:
        for item in messages:
            item["text_clean"] = cleaner.clean(item.get("text_raw", ""))
            message = Message(**item)
            session.add(message)

        session.commit()
    finally:
        session.close()


def fetch_all_messages() -> list[Message]:
    session = SessionLocal()
    try:
        return session.query(Message).all()
    finally:
        session.close()


def main() -> None:
    init_db()

    telegram_messages = TelegramCollector().collect()
    news_messages = NewsCollector().collect()

    all_messages = telegram_messages + news_messages
    save_messages(all_messages)

    print(f"Saved {len(all_messages)} messages to database.")

    messages = fetch_all_messages()
    texts = [msg.text_clean for msg in messages]

    feature_extractor = TfidfFeatureExtractor()
    vectors = feature_extractor.fit_transform(texts)

    similarity_engine = SimilarityEngine()
    similarity_matrix = similarity_engine.build_similarity_matrix(vectors)

    print("\nSimilarity matrix:")
    for row in similarity_matrix:
        print([round(float(value), 3) for value in row])

    pair_finder = SimilarPairFinder()
    pairs = pair_finder.find_pairs(messages, similarity_matrix, threshold=0.05)

    print("\nSimilar pairs:")
    if not pairs:
        print("No similar pairs found.")
    else:
        for pair in pairs:
            print(f"\nScore: {pair['score']:.3f}")
            print(f"1) {pair['message_1'].source_name}: {pair['message_1'].text_raw}")
            print(f"2) {pair['message_2'].source_name}: {pair['message_2'].text_raw}")

    baseline = StatisticalBaseline(similarity_threshold=0.05, min_neighbors=1)
    baseline_results = baseline.analyze(similarity_matrix)

    print("\nBaseline analysis:")
    for message, result in zip(messages, baseline_results):
        print(
            f"[{result['label']}] "
            f"neighbors={result['similar_neighbors']} "
            f"max_sim={result['max_similarity']} "
            f"avg_sim={result['avg_similarity']} "
            f"score={result['suspicion_score']} | "
            f"{message.source_name}: {message.text_raw}"
        )

    cluster_engine = ClusterEngine()
    cluster_labels = cluster_engine.cluster(similarity_matrix, eps=0.95, min_samples=2)

    print("\nCluster labels:")
    for message, label in zip(messages, cluster_labels):
        print(f"[cluster {label}] {message.source_name}: {message.text_raw}")


if __name__ == "__main__":
    main()
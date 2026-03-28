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
from app.evaluation.metrics import MetricsEvaluator
from app.labels.test_labels import TEST_LABELS, build_key


def save_messages(messages: list[dict]) -> tuple[int, int]:
    session = SessionLocal()
    cleaner = TextCleaner()
    inserted = 0
    skipped = 0

    try:
        for item in messages:
            existing = (
                session.query(Message)
                .filter(
                    Message.source_name == item["source_name"],
                    Message.external_id == item["external_id"],
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            item["text_clean"] = cleaner.clean(item.get("text_raw", ""))
            message = Message(**item)
            session.add(message)
            inserted += 1

        session.commit()
        return inserted, skipped
    finally:
        session.close()


def fetch_all_messages() -> list[Message]:
    session = SessionLocal()
    try:
        return session.query(Message).all()
    finally:
        session.close()


def build_true_labels(messages: list[Message]) -> list[int]:
    y_true = []

    for message in messages:
        key = build_key(message.source_name, message.external_id)
        label = TEST_LABELS.get(key, 0)
        y_true.append(label)

    return y_true


def main() -> None:
    init_db()

    telegram_messages = TelegramCollector().collect()
    news_messages = NewsCollector().collect()

    all_messages = telegram_messages + news_messages
    inserted, skipped = save_messages(all_messages)

    print(f"Inserted: {inserted}, skipped duplicates: {skipped}")

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
    y_pred = [item["label"] for item in baseline_results]

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

    y_true = build_true_labels(messages)

    evaluator = MetricsEvaluator()
    metrics = evaluator.evaluate(y_true, y_pred)

    print("\nEvaluation metrics:")
    print(f"y_true: {y_true}")
    print(f"y_pred: {y_pred}")
    print(f"Accuracy:  {metrics['accuracy']:.3f}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall:    {metrics['recall']:.3f}")
    print(f"F1-score:  {metrics['f1_score']:.3f}")
    print(f"Confusion matrix: {metrics['confusion_matrix']}")


if __name__ == "__main__":
    main()
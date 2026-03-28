TEST_LABELS = {
    "ukr_test_channel:101": 1,
    "ukr_test_channel:102": 0,
    "test_news_site:news-001": 1,
    "test_news_site:news-002": 0,
}


def build_key(source_name: str, external_id: str | None) -> str:
    return f"{source_name}:{external_id}"
from datetime import datetime, timedelta

from app.collectors.base_collector import BaseCollector


class NewsCollector(BaseCollector):
    def collect(self) -> list[dict]:
        now = datetime.now()

        return [
            {
                "source_type": "news",
                "source_name": "test_news_site",
                "external_id": "news-001",
                "title": "Новий пакет допомоги Україні",
                "text_raw": "Партнери оголосили про надання нового пакета допомоги Україні.",
                "url": "https://example.com/news-001",
                "published_at": now - timedelta(minutes=20),
                "collected_at": now,
            },
            {
                "source_type": "news",
                "source_name": "test_news_site",
                "external_id": "news-002",
                "title": "Безпекові ініціативи в Києві",
                "text_raw": "У столиці відбулася зустріч щодо нових безпекових ініціатив.",
                "url": "https://example.com/news-002",
                "published_at": now - timedelta(minutes=7),
                "collected_at": now,
            },
        ]
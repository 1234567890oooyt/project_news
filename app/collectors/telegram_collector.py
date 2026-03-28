from datetime import datetime, timedelta

from app.collectors.base_collector import BaseCollector


class TelegramCollector(BaseCollector):
    def collect(self) -> list[dict]:
        now = datetime.now()

        return [
            {
                "source_type": "telegram",
                "source_name": "ukr_test_channel",
                "external_id": "101",
                "title": None,
                "text_raw": "Україна отримала новий пакет допомоги від партнерів.",
                "url": "https://t.me/ukr_test_channel/101",
                "published_at": now - timedelta(minutes=10),
                "collected_at": now,
            },
            {
                "source_type": "telegram",
                "source_name": "ukr_test_channel",
                "external_id": "102",
                "title": None,
                "text_raw": "Сьогодні в Києві обговорили нові безпекові ініціативи.",
                "url": "https://t.me/ukr_test_channel/102",
                "published_at": now - timedelta(minutes=5),
                "collected_at": now,
            },
        ]
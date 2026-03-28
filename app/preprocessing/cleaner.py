import re


class TextCleaner:
    def clean(self, text: str | None) -> str:
        if not text:
            return ""

        text = text.lower()

        # прибираємо URL
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)

        # прибираємо telegram mention
        text = re.sub(r"@\w+", " ", text)

        # прибираємо зайві символи, лишаємо літери/цифри/пробіли
        text = re.sub(r"[^a-zA-Zа-яА-ЯіІїЇєЄґҐ0-9\s]", " ", text)

        # прибираємо зайві пробіли
        text = re.sub(r"\s+", " ", text).strip()

        return text
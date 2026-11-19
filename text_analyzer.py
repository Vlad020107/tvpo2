"""Детерминированный анализ текста без внешних зависимостей."""
import re
from collections import Counter


def _words(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", text.casefold())


def count_words(text: str) -> int:
    return len(_words(text))


def count_characters(text: str) -> int:
    return len(text)


def word_frequencies(text: str) -> dict[str, int]:
    return dict(Counter(_words(text)))


def most_common_word(text: str) -> str | None:
    frequencies = word_frequencies(text)
    if not frequencies:
        return None
    return min(frequencies, key=lambda word: (-frequencies[word], word))


def average_word_length(text: str) -> float:
    words = _words(text)
    if not words:
        return 0.0
    return sum(map(len, words)) / len(words)

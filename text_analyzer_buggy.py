"""Исходная версия: преднамеренная ошибка в count_words."""
from text_analyzer import count_characters, word_frequencies, most_common_word, average_word_length


def count_words(text: str) -> int:
    return len(text.split(" "))

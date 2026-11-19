import text_analyzer as analyzer


def test_count_words_simple():
    assert analyzer.count_words("кот пес") == 2


def test_count_words_multiple_spaces():
    assert analyzer.count_words("  кот   пес ") == 2


def test_count_characters_simple():
    assert analyzer.count_characters("Кот") == 3


def test_word_frequencies_repeated():
    assert analyzer.word_frequencies("cat cat dog") == {"cat": 2, "dog": 1}


def test_most_common_unique():
    assert analyzer.most_common_word("кот кот пес") == "кот"


def test_average_length_equal():
    assert analyzer.average_word_length("кот дом") == 3.0

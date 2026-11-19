import text_analyzer as analyzer


def test_characters_include_whitespace():
    assert analyzer.count_characters(" кот ") == 5


def test_casefold_normalizes_sharp_s():
    assert analyzer.word_frequencies("Straße STRASSE") == {"strasse": 2}


def test_most_common_tie_is_lexicographic():
    assert analyzer.most_common_word("кот пес") == "кот"


def test_average_length_fractional():
    assert analyzer.average_word_length("кот собака") == 4.5


def test_empty_inputs():
    assert analyzer.count_words("") == 0
    assert analyzer.count_characters("") == 0
    assert analyzer.word_frequencies("") == {}
    assert analyzer.most_common_word("") is None
    assert analyzer.average_word_length("") == 0.0


def test_punctuation_and_case():
    assert analyzer.count_words("КОТ, пёс!") == 2
    assert analyzer.word_frequencies("КОТ, кот!") == {"кот": 2}

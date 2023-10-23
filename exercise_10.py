import pytest


def test_len_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"The number of characters in the phrase is more than 15"

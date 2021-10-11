from .levels import Levels


def test_level_lookup():
    assert Levels.get_level_for_score(600) == 6


def test_level_lookup_at_threshold():
    assert Levels.get_level_for_score(9660) == 18


def test_level_lookup_max():
    assert Levels.get_level_for_score(100000) == 51

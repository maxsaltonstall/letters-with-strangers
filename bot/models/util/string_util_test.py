from string_util import StringUtil


def test_readable_list():
    assert StringUtil.readable_list(['foo', 'bar', 'baz']) == 'foo, bar, and baz'
    assert StringUtil.readable_list(['foo', 'bar'], 'bold') == '**foo** and **bar**'


def test_emoji_letter():
    assert StringUtil.emoji_letter('s') == ':regional_indicator_s:'


def test_format_player_xp():
    # note: the return from 'format_player_xp' is super complicated, so we'll just verify that we do indeed get a return
    formatted = StringUtil.format_player_xp(letter_xp={'a': 5, 'l': 99, 'n': 2, 't': 102, 'x': 2})
    assert len(formatted) > 0

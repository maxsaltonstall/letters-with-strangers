import pytest

from string_util import StringUtil

def test_readable_list():
    assert StringUtil.readable_list(['foo','bar','baz']) == 'foo, bar, and baz'
    assert StringUtil.readable_list(['foo','bar'], 'bold') == '**foo** and **bar**'

def test_emoji_letter():
    assert StringUtil.emoji_letter('s') == '🇸'

def test_format_player_xp():
    input = {'A':10,'B':5,'E':20,'N':4,'R':9}
    expected_output = '🇦 `  10`\u2000\u2000\u2000🇧 `   5`\u2000\u2000\u2000🇨 `   0`\u2000\u2000\u2000🇩 `   0`\u2000\u2000\u2000\n\n🇪 `  20`\u2000\u2000\u2000🇫 `   0`\u2000\u2000\u2000🇬 `   0`\u2000\u2000\u2000🇭 `   0`\u2000\u2000\u2000\n\n🇮 `   0`\u2000\u2000\u2000🇯 `   0`\u2000\u2000\u2000🇰 `   0`\u2000\u2000\u2000🇱 `   0`\u2000\u2000\u2000\n\n🇲 `   0`\u2000\u2000\u2000🇳 `   4`\u2000\u2000\u2000🇴 `   0`\u2000\u2000\u2000🇵 `   0`\u2000\u2000\u2000\n\n🇶 `   0`\u2000\u2000\u2000🇷 `   9`\u2000\u2000\u2000🇸 `   0`\u2000\u2000\u2000🇹 `   0`\u2000\u2000\u2000\n\n🇺 `   0`\u2000\u2000\u2000🇻 `   0`\u2000\u2000\u2000🇼 `   0`\u2000\u2000\u2000🇽 `   0`\u2000\u2000\u2000\n\n🇾 `   0`\u2000\u2000\u2000🇿 `   0`\u2000\u2000\u2000'
    assert StringUtil.format_player_xp(input) == expected_output
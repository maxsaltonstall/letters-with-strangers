from typing import List, Any
from collections import defaultdict


class StringUtil:
    @staticmethod
    def readable_list(seq: List[Any], format: str = '') -> str:
        """Return a grammatically correct human readable string (with an Oxford comma)."""
        # Ref: https://stackoverflow.com/a/53981846/
        seq = [str(s) for s in seq]
        if format == 'bold':
            seq = ['**' + str(s) + '**' for s in seq]
        if len(seq) < 3:
            return ' and '.join(seq)
        return ', '.join(seq[:-1]) + ', and ' + seq[-1]

    @staticmethod
    def emoji_letter(s: str) -> str:
        """Translate an ASCII character to an emoji character.
        """
        return f":regional_indicator_{s.lower()}:"

    @staticmethod
    def format_player_xp(letter_xp: dict, row_length: int = 4) -> str:
        """Receives a dict of a player's Letter XP points, and returns
           a string formatted for return as part of the 'progress' message."""
        letter_xp_string = ''
        letter_xp = defaultdict(int, letter_xp)
        for i in range(1, 27):
            letter = chr(i + 64)
            letter_xp_string += f"{StringUtil.emoji_letter(letter)} `{'{:4d}'.format(letter_xp[letter])}`\u2000\u2000\u2000"
            if i % row_length == 0:
                letter_xp_string += '\n\n'

        return letter_xp_string

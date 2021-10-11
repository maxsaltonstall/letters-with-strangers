class Levels:

    @staticmethod
    def get_level_for_score(score: int) -> int:
        level_table = {
            1: 0,
            2: 10,
            3: 50,
            4: 140,
            5: 300,
            6: 540,
            7: 860,
            8: 1260,
            9: 1740,
            10: 2300,
            11: 2940,
            12: 3660,
            13: 4460,
            14: 5340,
            15: 6300,
            16: 7340,
            17: 8460,
            18: 9660,
            19: 10940,
            20: 12300,
            21: 13740,
            22: 15260,
            23: 16860,
            24: 18540,
            25: 20300,
            26: 22140,
            27: 24060,
            28: 26060,
            29: 28140,
            30: 30300,
            31: 32540,
            32: 34860,
            33: 37260,
            34: 39740,
            35: 42300,
            36: 44940,
            37: 47660,
            38: 50460,
            39: 53340,
            40: 56300,
            41: 59340,
            42: 62460,
            43: 65660,
            44: 68940,
            45: 72300,
            46: 75740,
            47: 79260,
            48: 82860,
            49: 86540,
            50: 90300,
            51: 94140
        }
        for level in level_table:
            if level < len(level_table) and score >= level_table[level] and score < level_table[level + 1]:
                return level
        # if we get here, we've exceeded the levels in the levels table
        return list(level_table)[-1]

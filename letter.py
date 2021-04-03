import random, string


class Letter:
    letter_weight = {  # each integer = percent chance * 10 to appear, 100 = 10%
        "A": 85, "B": 20, "C": 45, "D": 34, "E": 112, "F": 18, "G": 25, "H": 30, "I": 75, "J": 2,
        "K": 11, "L": 55, "M": 30, "N": 67, "O": 72, "P": 32, "Q": 2, "R": 76, "S": 57, "T": 69,
        "U": 36, "V": 10, "W": 13, "X": 2, "Y": 18, "Z": 2
    }
    
    @staticmethod
    # Give a semi-random letter, to help people make words
    # TODO: Match proper frequencies for english words, see weight matrix above
    def random_letter():
        ltr = ''
        r = random.randint(1, 13)
        if r == 1 or r == 2:
            ltr = 'E'
        elif r == 3:
            ltr = 'A'
        elif r == 4:
            ltr = 'R'
        elif r == 5:
            ltr = 'T'
        elif r == 6:
            ltr = 'N'
        elif r == 7:
            ltr = 'S'
        elif r == 8:
            ltr = 'L'
        elif r == 9:
            ltr = 'I'
        else:
            ltr = random.choice(string.ascii_uppercase)
        return ltr

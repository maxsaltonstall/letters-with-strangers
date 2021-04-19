import logging


class Dictionary:

    lexicon = "uninitialized"

    def __init__(self, lexicon):
        self.lexicon = lexicon
        if lexicon == "simple":
            self.words_i_know = frozenset(['CAT', 'RAT', 'BAT', 'SAT', 'MAT', 'TALL', 'BALL', 'CALL', 'FALL', 'FAR', 'TAR',
                                           'BAR', 'CAR', 'CAB', 'TAB', 'LAB', 'GNAT', 'TAN', 'CAN', 'BAN', 'RAN', 'BASS',
                                           'MAN', 'APP', 'TART', 'FART', 'THAT', 'SEEN', 'LANE', 'TEEN', 'TALE', 'TEAL', 'FELL',
                                           'TELL', 'SET', 'NET', 'EAT', 'BEAT', 'NEAT', 'SEAT', 'TEAR', 'STAR', 'LANE', 'ARE',
                                           'SELL', 'SALE', 'SEAL', 'LEER', 'STELLAR', 'TREE', 'SEER', 'PEER', 'PEAR', 'APE',
                                           'TINE', 'SINE', 'SIN', 'NIT', 'RISE', 'LINT', 'TILL', 'SILL', 'TIN', 'TIRE', 'AND',
                                           'END', 'SAND', 'SEND', 'TEND', 'STAND', 'LET', 'TEN', 'RITE', 'BITE', 'SITE', 'LIT',
                                           'FIT', 'SIT', 'TIT', 'TAT', 'PAT', 'STALL', 'TEST', 'SEE', 'SEA', 'TEE', 'TEA', 'LEE',
                                           'TEAT', 'SEAR', 'STILL', 'STOLE', 'SNARL', 'TARNISH', 'TAIL', 'SAIL', 'FAIL', 'SALT',
                                           'TILT', 'STEAL', 'STEEL', 'TENT', 'TENET', 'RAIN', 'REIN', 'EAST', 'RAIL', 'TRELLIS',
                                           'FILTER', 'TOLL', 'SOLE', 'MAIL', 'NAIL', 'RID', 'ROD', 'COD', 'ROT', 'RINSE'])

        elif lexicon == "sowpods":
            self.words_i_know = []
            with open('data/dictionaries/sowpods.raw.txt') as file:
                lines = file.read().splitlines()
                for line in lines:
                    self.words_i_know.append(line)
            self.words_i_know = frozenset(self.words_i_know)
        
        else:
            self.words_i_know = []
        
        logging.info(f"Dictionary loaded! It contains {len(self.words_i_know)} words")

    def check_word(self, word):
        return word in self.words_i_know

    def __str__(self):
        return self.lexicon

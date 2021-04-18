import logging, jsonpickle, random, os
from collections import defaultdict

from .dictionary import Dictionary
from .party import Party


class Player:

    def __init__(self, user):
        
        self.player_id = user.id
        self.statefile = f".lws/player_{self.player_id}.json"
        
        try:
            with open(self.statefile, 'r') as statefile:
                self.state = jsonpickle.decode(statefile.read())
        except FileNotFoundError:
            logging.debug(f"statefile not found; initializing statefile for {self.player_id}")
            self.state = {}
            self.state["username"] = user.name
            self.state["letters"] = []
            self.state["score"] = 0  # experience
            self.state["money"] = 0  # currency
            self.state["handlimit"] = 8  # default for new players
            self.state["letter_xp"] = defaultdict(int)  # track progress per letter + wildcard
            self.save_state()

    def form_party(self, members):
        if "party" in self.state:
            # I'm already in a party; add new members to it
            party = Party(party_id=self.state["party"])
            for member in members:
                party.add_member(member)
            return(party)
        else:
            members.append(self.player_id)
            party = Party()
            for member in members:
                party.add_member(member)
            self.state["party"] = party.get_id()
            self.save_state()
            return(party)
    
    def get_party(self):
        if "party" in self.state:
            return(f"{Party(self.state['party'])}")
        else:
            return("You're not currently in a party. Start one with: `..party @User1 @User2`")

    def leave_party(self):
        message = Party(self.state["party"]).remove_member(self.player_id)
        del self.state["party"]
        self.save_state()
        return message
    
    def get_letters(self):
        return self.state["letters"]

    def add_letter(self, letter):
        if self.num_letters() >= self.state["handlimit"]:
            return(f"{self.state['username']}, you already have a full hand of letters")
        else:
            self.state["letters"].append(letter)
            self.save_state()
            return(f"{self.state['username']}, you can have a {letter}")

    def cheat(self):  # for testing/developing
        try:
            self.state["letters"] = ["A", "E", "I", "L", "N", "R", "S", "T"]
            self.state["money"] += 1000
            self.save_state()
            return("Your hand is now: A, E, I, L, N, R, S, and T!")
        except Exception as e:
            logging.error("# Error 4 #: Error when cheating in letters")
            logging.exception(str(e))
            return("Unable to help you cheat, cheaty!")

    def purge(self):  # for testing/developing
        self.state["letters"] = []
        self.save_state()
        return("Poof! All your letters are gone.")

    def remove_letter(self, letter):
        self.state["letters"].remove(letter.upper())
        self.save_state()

    def remove_letters(self, letters):
        for letter in letters:
            self.remove_letter(letter)

    def shuffle_letters(self):
        random.shuffle(self.state["letters"])
        self.save_state()
        return(f"Shuffled your letters! They are now {self.state['letters']}")

    def num_letters(self):
        return len(self.state["letters"])

    def get_username(self):
        return self.state["username"]

    def add_points(self, points):
        self.state["score"] += points
        self.save_state()

    def get_score(self):
        return self.state["score"]

    def add_money(self, cash):
        self.state["money"] += cash
        self.save_state()
               
    def get_money(self):
        return self.state["money"]

    def make_word(self, word: str, dictionary: Dictionary):
        if dictionary.check_word(word):
            points = len(word)
            self.add_points(points)
            self.add_money(points)
            unique_letters = ''.join(set(word))
            for letter in unique_letters:
                try:
                    self.remove_letter(letter)
                except:
                    return f"unable to spell the word {word}; you don't have the letter '{letter}'"
            return f"you formed the word '{word}' and scored {points} points"
        else:
            logging.info(f"Word '{word}' not found in dictionary {dictionary}")
            return f"Sorry, the word '{word}' isn't in my vocabulary!"

    def save_state(self):
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        pickled = jsonpickle.encode(self.state)
        with open(self.statefile, 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    def __str__(self):
        return self.get_username()

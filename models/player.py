import logging, random
from collections import defaultdict

from .letter import Letter
from .util.string_util import StringUtil
from .util.datastore import save_player, load_player


class Player:

    def __init__(self, user=None):
        
        if user:
            
            self.player_id = user.id
            
            player_state = self.read_state(self.player_id)  # try loading player state from storage

            if player_state:
                self.state = player_state
            else:  # create new user
                self.state = {}
                self.state["username"] = user.name
                self.state["letters"] = []
                self.state["score"] = 0  # experience
                self.state["money"] = 0  # currency
                self.state["handlimit"] = 8  # default for new players
                self.state["letter_xp"] = defaultdict(int)  # track progress per letter + wildcard
                self.save_state()
        else:  # create empty object
            self.player_id = None
            self.state = None

    def get_id(self) -> int:
        return self.player_id

    def read_state(self, player_id: int) -> dict:
        return load_player(player_id)

    def save_state(self):
        save_player(self.player_id, self.state)

    @classmethod
    def load(cls, player_id: int) -> object:
        player = cls()
        player.player_id = player_id
        player.state = load_player(player.player_id)
        return player

    def set_party_id(self, party_id: int) -> None:
        self.state["party"] = party_id
        self.save_state()

    def get_party_id(self) -> int:
        if "party" in self.state:
            return self.state['party']
        else:
            return None

    def unset_party_id(self) -> None:
        if "party" in self.state:
            del self.state["party"]
            self.save_state()
    
    def get_letters(self):
        return self.state["letters"]

    def add_letter(self):
        if len(self.get_letters()) >= self.state["handlimit"]:
            return(f"{self.state['username']}, you already have a full hand of letters")
        else:
            letter = Letter.random_letter(restricted_letters=self.get_letters())
            self.state["letters"].append(letter)
            self.save_state()
            if letter in ('A', 'E', 'I', 'O', 'U'):
                return(f"{self.state['username']}, you can have an **{letter}**")
            return(f"{self.state['username']}, you can have a **{letter}**")

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

    def remove_letter(self, letter: str):
        if letter.upper() in self.state["letters"]:
            self.state["letters"].remove(letter.upper())
            self.save_state()

    def remove_letters(self, letters: list):
        for letter in letters:
            if letter in self.state["letters"]:
                self.state["letters"].remove(letter)
        self.save_state()

    def shuffle_letters(self):
        random.shuffle(self.state["letters"])
        self.save_state()
        return(f"Shuffled your letters! They are now {StringUtil.readable_list(self.state['letters'], 'bold')}")

    def get_username(self):
        return self.state["username"]

    def add_points(self, points):
        self.state["score"] += points
        self.save_state()

    def get_score(self):
        return self.state["score"]

    def add_letter_xp(self, letter, points):
        self.state["letter_xp"][letter] += points
        self.save_state()

    def get_letter_xp(self):
        return self.state["letter_xp"]

    def add_money(self, cash):
        self.state["money"] += cash
        self.save_state()
               
    def get_money(self):
        return self.state["money"]

    def get_mention_tag(self) -> str:
        """return a string which, when passed in a discord message,
           will render as this player's nickname"""
        return "<@!" + str(self.get_id()) + ">"

    def __str__(self):
        return self.get_username()

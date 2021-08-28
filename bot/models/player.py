import logging, random

import discord

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
                # TIP: use only data types that can be natively stored in Cloud Datastore (e.g. don't use defaultdict)
                self.state = {}
                self.state["username"] = user.name
                self.state["letters"] = []
                self.state["score"] = 0  # experience for advancing level
                self.state["money"] = 10  # currency to spend on stuff, so you can buy letters
                self.state["level"] = 1  # long term advancement
                self.state["handlimit"] = 8  # default for new players
                self.state["letter_xp"] = {}  # track progress per letter + wildcard
                self.state["longest_word"] = ""  # best creation
                self.state["pets"] = []
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

    def add_vowel(self):
        if len(self.get_letters()) >= self.state["handlimit"]:
            return(f"{self.state['username']}, you already have a full hand of letters")
        else:
            letter = Letter.random_letter(restricted_letters=['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'])
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

    async def show_progress(self, ctx):

        letter_xp_string = StringUtil.format_player_xp(self.get_letter_xp())

        try:
            lvl = self.get_level()
        except Exception as e:
            logging.error("# Error 5 #: Error when getting player level")
            logging.exception(str(e))
            lvl = 1

        embed = discord.Embed(
            title=f"Player profile: {self.get_username()}",
            description=f"""
                ...................................................
                Level: **{lvl}**
                Score: **{self.get_score()}**
                Glyphs: **{self.get_money()}**
                ...................................................
                """
        )
        embed.add_field(
            name="Letter XP:",
            value=f"{letter_xp_string}",
            inline=False)
        
        await ctx.send(embed=embed)

    def add_letter_xp(self, letter, points):
        if letter in self.state["letter_xp"]:
            self.state["letter_xp"][letter] += points
        else:
            self.state["letter_xp"][letter] = 1
        self.save_state()

    def get_letter_xp(self):
        return self.state["letter_xp"]

    def add_money(self, cash):
        self.state["money"] += cash
        self.save_state()

    def get_level(self):
        return self.state["level"]

    def get_money(self):
        return self.state["money"]

    def get_mention_tag(self) -> str:
        """return a string which, when passed in a discord message,
           will render as this player's nickname"""
        return "<@!" + str(self.get_id()) + ">"

    def __str__(self):
        return self.get_username()

import logging, random

import discord

from .letter import Letter
from .levels import Levels
from .util.string_util import StringUtil
from .util.datastore import save_player, load_player


class Player:

    def __init__(self, player=None):
        
        if player:
            
            self.player_id = player.id
            
            player_state = self.read_state(self.player_id)  # try loading player state from storage

            if player_state:
                self.state = player_state
            else:  # create new player
                # TIP: use only data types that can be natively stored in Cloud Datastore (e.g. don't use defaultdict)
                self.state = {}
                self.state["username"] = player.name
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

    def leave_party(self) -> str:
        party_id = self.get_party_id()
        if party_id:
            del self.state["party"]
            self.save_state()
            try:
                from .party import Party
                party = Party(party_id)
                party.remove_member(self.get_id())
            except Exception as e:
                # something went wrong, but we were able to remove the user's party ID. So log it and move on.
                logging.error(f"Unable to remove member {self.get_id()} from party {party_id} [{str(e)}]")
            return "You've left that party."
        else:
            return "You're not in a party! Start one with `..party @username1 @username2`"
        
    def get_letters(self):
        return self.state["letters"]

    def num_letters_in_hand(self) -> int:
        return len(self.state["letters"])

    def get_handlimit(self) -> int:
        return self.state["handlimit"]

    def add_letters(self, letter_type: str = '', quantity: int = 1) -> str:
        new_letters = []
        letters_in_hand = self.get_letters()
        for i in range(quantity):
            letter = Letter.random_letter(letter_type=letter_type, restricted_letters=letters_in_hand)
            new_letters.extend(letter)
            letters_in_hand.extend(letter)
        self.save_state()

        if quantity == 1:
            letter_added = new_letters[0]
            article = 'an' if letter_added in ('A', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'R', 'S', 'X') else 'a'
            return f"{self.get_username()}, you can have {article} **{letter_added}**"
        else:
            return f"{self.get_username()}, you can have {StringUtil.readable_list(new_letters, format='bold')}"

    def cheat(self):  # for testing/developing
        try:
            self.state["letters"] = ["A", "E", "I", "L", "N", "R", "S", "T"]
            self.state["money"] += 1000
            self.save_state()
            return("Your hand is now: A, E, I, L, N, R, S, and T!")
        except Exception as e:
            logging.error(f"# Error 4 #: Error when cheating in letters: {str(e)}")
            return("Unable to help you cheat, cheaty!")

    def purge(self):  # for testing/developing
        self.state["letters"] = []
        self.save_state()
        return("Poof! All your letters are gone.")

    def remove_letters(self, letters: list):
        for letter in letters:
            if letter.upper() in self.state["letters"]:
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
        self.state["level"] = Levels.get_level_for_score(self.get_score())
        self.save_state()

    def add_points_and_check_for_levelup(self, points: int) -> int:
        """if player has leveled up, return new level. Else return None"""
        old_level = self.get_level()
        self.add_points(points)
        logging.debug(f"points: {self.get_score()}; level: {self.get_level()}")
        return None if self.get_level() == old_level else self.get_level()

    def get_score(self):
        return self.state["score"]

    async def show_progress(self, ctx):

        letter_xp_string = StringUtil.format_player_xp(self.get_letter_xp())

        embed = discord.Embed(
            title=f"Player profile: {self.get_username()}",
            description=f"""
                ...................................................
                Level: **{self.get_level()}**
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

    def check_money(self, amount):
        if self.get_money() >= amount:
            return True
        else:
            return False

    def deduct_money(self, amount):
        if self.get_money() < amount:
            raise ValueError(f"Unable to deduct {amount} from player {self.get_id()}; their balance is only {self.get_money()}")
        else:
            self.state["money"] -= amount
            self.save_state()

    def get_level(self):
        try:
            lvl = self.state["level"]
        except Exception as e:
            logging.error(f"# Error 5 #: Error when getting player level: {str(e)}")
            lvl = 1
        return lvl

    def get_money(self):
        return self.state["money"]

    def get_mention_tag(self) -> str:
        """return a string which, when passed in a discord message,
           will render as this player's nickname"""
        return "<@!" + str(self.get_id()) + ">"

    def __str__(self):
        return self.get_username()

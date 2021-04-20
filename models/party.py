import logging, jsonpickle, uuid, os

from .dictionary import Dictionary
from .player import Player

from .util.string_util import StringUtil


class Party:

    def __init__(self, party_id: str = ''):
        if party_id:
            self.party_id = party_id
            with open(Party.statefile(party_id), 'r') as statefile:
                self.state = jsonpickle.decode(statefile.read())
        else:
            self.state = {}
            self.state["members"] = set()  # list of member IDs
            self.party_id = uuid.uuid4().hex
            self.save_state()
            logging.info(f"initialized party {self.party_id}: {str(self.state['members'])}")

    @staticmethod
    def statefile(party_id: int):
        return f".lws/party_{party_id}.json"

    def save_state(self):
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        pickled = jsonpickle.encode(self.state)
        with open(Party.statefile(self.party_id), 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    def get_id(self) -> int:
        return self.party_id

    def add_members(self, members: list[object]) -> str:
        members_added = []
        already_partying_members = []
        for member in members:
            player = Player(member)
            if player.get_party_id() and player.get_party_id() != self.get_id():
                # player is in another party
                already_partying_members.append(player.get_mention_tag())
            else:
                self.state["members"].add(player.get_id())
                player.set_party_id(self.get_id())
                members_added.append(player.get_mention_tag())
        self.save_state()
        msg = ""
        if len(members_added):
            msg += f"Added {StringUtil.readable_list(members_added)} to your party. "
        if len(already_partying_members):
            msg += f"Couldn't add {StringUtil.readable_list(already_partying_members)} -- they're already in another party!"
        return msg

    def remove_member(self, member_id: int) -> str:
        try:
            self.state["members"].remove(member_id)
            self.save_state()
            if len(self.get_members()) <= 1:
                self.disband_party()
            return "You've left that party."
        except ValueError:
            return "Error: member not found in party"

    def disband_party(self) -> None:
        for player_id in self.get_members():
            player = Player.load(player_id)
            player.unset_party_id()
        os.remove(Party.statefile(self.get_id()))

    def get_members(self) -> list:
        return list(self.state["members"])

    def get_members_as_string(self) -> str:
        player_names = []
        for player_id in self.get_members():
            player = Player.load(player_id)
            player_names.append(player.get_mention_tag())
        return StringUtil.readable_list(player_names)

    def get_letters(self) -> list:
        party_letters = set()
        for player_id in self.get_members():
            player = Player.load(player_id)
            for letter in player.get_letters():
                party_letters.add(letter)

        list_party_letters = list(party_letters)
        list_party_letters.sort()

        return list_party_letters

    def make_word(self, word: str, dictionary: Dictionary) -> str:
        
        if not dictionary.check_word(word):
            logging.info(f"Word '{word}' not found in dictionary {dictionary}")
            return f"Sorry, the word '{word}' isn't in my vocabulary!"
        
        letters = list(word)
        missing_letters = []
        for letter in letters:
            if letter not in self.get_letters():
                missing_letters.append(letter)
        missing_letters = list(set(missing_letters))
        missing_letters.sort()
        if len(missing_letters):
            return f"unable to spell the word {word}; you don't have the letter(s) {StringUtil.readable_list(missing_letters, 'bold')}"
        points = len(word)
        for player_id in self.get_members():
            player = Player.load(player_id)
            player.remove_letters(letters)
            player.add_points(points)
        return f"you formed the word '{word}' and {' everyone' if len(self.get_members()) > 1 else ''} scored {points} points"

    def __str__(self):
        return f"Party members: {self.get_members_as_string()}"

import logging, jsonpickle, uuid, os

from .dictionary import Dictionary
from .player import Player

from .util.string_util import StringUtil


class Party:

    def __init__(self, party_id: str = ''):
        if party_id:
            self.party_id = party_id
            self.statefile = f".lws/party_{self.party_id}.json"
            with open(self.statefile, 'r') as statefile:
                self.state = jsonpickle.decode(statefile.read())
        else:
            self.state = {}
            self.state["members"] = []  # list of member IDs
            self.party_id = uuid.uuid4().hex
            self.save_state()
            logging.info(f"initialized party {self.party_id}: {str(self.state['members'])}")

    def save_state(self):
        statefile = f".lws/party_{self.party_id}.json"
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        pickled = jsonpickle.encode(self.state)
        with open(statefile, 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    def get_id(self) -> int:
        return self.party_id

    def add_member(self, member_id: int) -> str:
        new_member = Player.load(member_id)
        new_member_prior_party_id = new_member.get_party_id()
        if new_member_prior_party_id == self.get_id():
            return f"{new_member.get_username()} is already in your party"
        elif not new_member_prior_party_id:
            self.state["members"].append(member_id)
            self.save_state()
            return f"added {new_member.get_username()} to your party"
        elif new_member_prior_party_id != self.get_id():
            return f"Can't add {new_member.get_username()} to your party -- they're already in another party!"

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
        os.remove(self.statefile)

    def get_members(self) -> list:
        return self.state["members"]

    def get_members_as_string(self) -> str:
        player_names = []
        for player_id in self.get_members():
            player = Player.load(player_id)
            player_names.append(player.get_username())
        return StringUtil.readable_list(player_names, 'bold')

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
        if dictionary.check_word(word):
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
        else:
            logging.info(f"Word '{word}' not found in dictionary {dictionary}")
            return f"Sorry, the word '{word}' isn't in my vocabulary!"

    def __str__(self):
        return f"Party members: {self.get_members_as_string()}"

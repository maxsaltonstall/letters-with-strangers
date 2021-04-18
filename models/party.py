import logging, jsonpickle, uuid

from .util.player_util import PlayerUtil
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

    def add_member(self, member_id: int):
        self.state["members"].append(member_id)
        self.save_state()

    def get_members(self):
        return self.state["members"]

    def get_members_as_string(self) -> str:
        player_names = [PlayerUtil.get_player_username_by_id(player) for player in self.get_members()]
        return StringUtil.readable_list(player_names)

    def __str__(self):
        return f"Party {self.party_id}: **{self.get_members_as_string()}**"

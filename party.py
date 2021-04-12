import logging, jsonpickle, uuid


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
        pickled = jsonpickle.encode(self.state)
        with open(statefile, 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    def add_member(self, member: int):
        self.state["members"].append(member)
        self.save_state()

    def get_members(self):
        return self.state["members"]

    def __str__(self):
        return str(self.party_id)

import logging, jsonpickle


class Player:

    def __init__(self, user):
        
        self.player_id = f"{user.name}#{user.discriminator}"
        self.statefile = f".lws/{self.player_id}.json"
        
        try:
            with open(self.statefile, 'r') as statefile:
                self.state = jsonpickle.decode(statefile.read())
        except FileNotFoundError:
            logging.debug(f"statefile not found; initializing statefile for {self.name}")
            self.state = {}
            self.state["username"] = user.name
            self.state["letters"] = []
            self.state["score"] = 0
            self.save_state()

    def get_letters(self):
        return self.state["letters"]

    def add_letter(self, letter):
        self.state["letters"].append(letter)
        self.save_state()

    def cheat(self):
        try:
            self.remove_all_letters()
            for ltr in ["E", "A", "I", "S", "T", "L", "N", "R"]:
                self.add_letter(ltr)
            return("Your hand is now: E, A, I, S, T, L, N, and R!")
        except:
            logging.error("# Error 4 #: Error when cheating in letters")
            return("Unable to help you cheat, cheaty!")

    def remove_letter(self, letter):
        self.state["letters"].remove(letter.upper())
        self.save_state()

    def remove_letters(self, letters):
        for letter in letters:
            self.remove_letter(letter)

    def remove_all_letters(self):
        self.state["letters"] = []
        self.save_state()

    def num_letters(self):
        return len(self.state["letters"])

    def get_username(self):
        return self.state["username"]

    def add_points(self, points):
        self.state["score"] += points
        self.save_state()

    def get_score(self):
        return self.state["score"]

    def save_state(self):
        pickled = jsonpickle.encode(self.state)
        with open(self.statefile, 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    def __str__(self):
        return self.get_username()

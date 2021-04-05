import logging, jsonpickle, random


class Player:

    def __init__(self, user):
        
        self.player_id = f"{user.name}#{user.discriminator}"
        self.statefile = f".lws/{self.player_id}.json"
        
        try:
            with open(self.statefile, 'r') as statefile:
                self.state = jsonpickle.decode(statefile.read())
        except FileNotFoundError:
            logging.debug(f"statefile not found; initializing statefile for {self.player_id}")
            self.state = {}
            self.state["username"] = user.name
            self.state["letters"] = []
            self.state["score"] = 0
            self.state["handlimit"] = 8  # default for new players
            self.save_state()

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

    def save_state(self):
        pickled = jsonpickle.encode(self.state)
        with open(self.statefile, 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    def __str__(self):
        return self.get_username()

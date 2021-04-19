import os, logging, jsonpickle

class PlayerUtil:

    @staticmethod
    def load_playerstate(player_id:int) -> dict:
        statefile = f".lws/player_{player_id}.json"
        if os.path.exists(statefile):
            with open(statefile,'r') as statefile:
                player_state = jsonpickle.decode(statefile.read())
            return player_state
        else:
            logging.exception(f"unable to read statefile for user ID: {player_id}")

    @staticmethod
    def save_playerstate(player_id: int, state:dict):
        statefile = f".lws/player_{player_id}.json"
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        pickled = jsonpickle.encode(state)
        with open(statefile, 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    @staticmethod
    def get_player_username_by_id(id:int) -> str:
       state = PlayerUtil.load_playerstate(id)
       return state["username"]

    @staticmethod
    def get_player_letters(player_id:int) -> list:
        state = PlayerUtil.load_playerstate(player_id)
        return state["letters"]

    @staticmethod
    def remove_letters(player_id:int, letters_to_remove:list):
        state = PlayerUtil.load_playerstate(player_id)
        state["letters"] = [letter for letter in state["letters"] if letter not in letters_to_remove]
        PlayerUtil.save_playerstate(player_id, state)

    @staticmethod
    def add_points(player_id:int, points:int):
        state = PlayerUtil.load_playerstate(player_id)
        state["score"] += points
        PlayerUtil.save_playerstate(player_id, state)

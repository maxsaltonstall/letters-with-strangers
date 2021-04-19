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
    def get_player_username_by_id(id:int) -> str:
       state = PlayerUtil.load_playerstate(id)
       return state["username"]

    @staticmethod
    def get_player_letters(player_id:int) -> list:
        state = PlayerUtil.load_playerstate(player_id)
        return state["letters"]

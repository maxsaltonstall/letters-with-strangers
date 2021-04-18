import os, logging, jsonpickle

class PlayerUtil:
    @staticmethod
    def get_player_username_by_id(id:int):
        statefile = f".lws/player_{id}.json"
        if os.path.exists(statefile):
            with open(statefile,'r') as statefile:
                player_state = jsonpickle.decode(statefile.read())
            return player_state["username"]
        else:
            logging.error(f"unable to read statefile for user ID: {id}")
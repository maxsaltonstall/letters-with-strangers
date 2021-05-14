import os, jsonpickle, logging

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def data_storage() -> str:
    # where is the state data stored? (default = local disk)
    return os.environ.get("DATA_STORAGE", "local")


# for local data storage, return location of files
def player_statefile(player_id: int) -> str:
    return f".lws/player_{player_id}.json"


def party_statefile(party_id: int) -> str:
    return f".lws/party_{party_id}.json"


# for Firebase Realtime DB, initialize DB
def init_db():
    if not firebase_admin._apps:  # if not already initialized
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('creds/firebase.json')
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': data_storage()
        })


def save_player(player_id: int, player_state: dict):

    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    pickled = jsonpickle.encode(player_state)

    if data_storage() == "local":
        with open(player_statefile(player_id), 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    else:  # store state in Firebase Realtime DB
        init_db()
        ref = db.reference(f'/player/{player_id}')
        ref.set(pickled)


def load_player(player_id: int) -> dict:

    if data_storage() == "local":
        statefile = player_statefile(player_id)
        if os.path.exists(statefile):
            with open(statefile, 'r') as statefile:
                return jsonpickle.decode(statefile.read())
        else:
            return None

    else:
        # load from firebase
        init_db()
        ref = db.reference(f'/player/{player_id}')
        player = ref.get()

        logging.debug(player)

        if player:
            return jsonpickle.decode(player)
        else:
            return None


def save_party(party_id: int, party_state: dict):
    
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    pickled = jsonpickle.encode(party_state)

    if data_storage() == "local":
        
        with open(party_statefile(party_id), 'w') as statefile:
            statefile.write(pickled)
            statefile.close()
    
    else:
        init_db()
        ref = db.reference(f'/party/{party_id}')
        ref.set(pickled)


def load_party(party_id: int) -> dict:

    if data_storage() == "local":

        statefile = party_statefile(party_id)
        if os.path.exists(statefile):
            with open(statefile, 'r') as statefile:
                return jsonpickle.decode(statefile.read())
        else:
            return None

    else:
        # load from firebase
        init_db()
        ref = db.reference(f'/party/{party_id}')
        party = ref.get()

        logging.debug(party)

        if party:
            return jsonpickle.decode(party)
        else:
            return None

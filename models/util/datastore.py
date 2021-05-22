import os, jsonpickle, logging
from google.cloud import firestore
from google.cloud.firestore_v1.document import DocumentReference




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
    return firestore.Client()


# get reference to firestore document
def get_db_ref(doc_type: str) -> DocumentReference:
    
    db = init_db()

    firestore_collection = os.environ.get("FIRESTORE_COLLECTION")

    if doc_type == 'player':
        return db.collection(firestore_collection).document("player_{player_id}")
    elif doc_type == 'party':
        return db.collection(firestore_collection).document("party_{party_id}")
    else:
        raise Exception("ERROR: unknown doc type requested from database")


def save_player(player_id: int, player_state: dict):

    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    pickled = jsonpickle.encode(player_state)

    if data_storage() == "local":
        with open(player_statefile(player_id), 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    elif data_storage() == "firebase":  # store state in Firestore
        
        ref = get_db_ref('player')
        ref.set(pickled)
    
    else:
        raise Exception("ERROR: no data storage configuration specified.")


def load_player(player_id: int) -> dict:

    if data_storage() == "local":
        statefile = player_statefile(player_id)
        if os.path.exists(statefile):
            with open(statefile, 'r') as statefile:
                return jsonpickle.decode(statefile.read())
        else:
            return None

    elif data_storage() == "firestore":  # load state from Firestore
    
        ref = get_db_ref('player')
        player = ref.get()

        logging.debug(player)

        if player:
            return jsonpickle.decode(player)
        else:
            return None

    else:
        raise Exception("ERROR: no data storage configuration specified.")


def save_party(party_id: int, party_state: dict):
    
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    pickled = jsonpickle.encode(party_state)

    if data_storage() == "local":
        
        with open(party_statefile(party_id), 'w') as statefile:
            statefile.write(pickled)
            statefile.close()
    
    else:
        ref = get_db_ref('party')
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
        # load from firestore
        ref = get_db_ref('party')
        party = ref.get()

        logging.debug(party)

        if party:
            return jsonpickle.decode(party)
        else:
            return None

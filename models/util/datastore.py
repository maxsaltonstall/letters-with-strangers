import os, jsonpickle, logging
from google.cloud import datastore




def data_storage() -> str:
    # where is the state data stored? (default = local disk)
    return os.environ.get("DATA_STORAGE", "local")


# for local data storage, return location of files
def player_statefile(player_id: int) -> str:
    return f".lws/player_{player_id}.json"


def party_statefile(party_id: int) -> str:
    return f".lws/party_{party_id}.json"


def get_db_client():
    if os.environ.get("DATASTORE_NAMESPACE"):
        client = datastore.Client(namespace=os.environ.get("DATASTORE_NAMESPACE"))
    else:
        client = datastore.Client()
    
    return client

def save_player(player_id: int, player_state: dict):

    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    pickled = jsonpickle.encode(player_state)

    if data_storage() == "local":
        with open(player_statefile(player_id), 'w') as statefile:
            statefile.write(pickled)
            statefile.close()

    elif data_storage() == "datastore":  # store state in Datastore
        
        client = get_db_client()
        player_record = datastore.Entity(client.key("Player", player_id))
        player_record.update(player_state)
        client.put(player_record)
    
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

    elif data_storage() == "datastore":  # load state from Datastore
    
        client = get_db_client()
        player_state = client.get(client.key("Player", player_id))

        if player_state:
            return player_state
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
        client = get_db_client()
        party_record = datastore.Entity(client.key("Party", party_id))
        party_record.update(party_state)


        logging.debug(party_state)
        client.put(party_record)


def load_party(party_id: int) -> dict:

    if data_storage() == "local":

        statefile = party_statefile(party_id)
        if os.path.exists(statefile):
            with open(statefile, 'r') as statefile:
                return jsonpickle.decode(statefile.read())
        else:
            return None

    else:
        # load from Datastore
        client = get_db_client()
        party_state = client.get(client.key("Party", party_id))

        if party_state:
            return party_state
        else:
            return None

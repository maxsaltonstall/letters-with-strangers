import os, jsonpickle, hashlib
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
    # if there's a datastore namespace specified in config, use it; otherwise, make one based on a hash of the discord token
    namespace = os.environ.get("DATASTORE_NAMESPACE", "autogenerated")
    if namespace == "autogenerated":
        namespace = hashlib.md5(os.environ.get("TOKEN").encode("utf-8")).hexdigest()

    return datastore.Client(namespace=namespace)
    

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


def disband_party(party_id: int):

    party_state = load_party(party_id)

    if party_state and party_state["members"]:
        players = party_state["members"]
        for player_id in players:
            player_state = load_player(player_id)
            del player_state['party']
            save_player(player_id, player_state)

    if data_storage() == "local":
        os.remove(party_statefile(party_id))
    else:
        client = get_db_client()
        party_record = datastore.Entity(client.key("Party", party_id))
        client.delete(party_record)

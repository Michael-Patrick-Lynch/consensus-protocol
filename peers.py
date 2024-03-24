from socket import *
# Added these lines - might need to change them later
from main import list_of_peers
from nodes import node_is_peer
# Maybe we could use json to send objects?
import json


# For testing
#list_of_peers = ['a', '1', '7']
#different_list_of_peers = ['9', '12', '14','a', '18']


# Gets rid of the peers in list_of_peers (except for this/our node) and adds the peers in
# different_list_of_peers to list_of_peers
def new_list_of_peers(different_list_of_peers):
    # Save this/our node (which is the first entry in list_of_peers)
    our_node = list_of_peers[0]
    # Delete the elements in list_of_peers
    list_of_peers.clear()
    # Add our_node to the start of list_of_peers
    list_of_peers.insert(0, our_node)
    # temp_list stores the elements in different_list_of_peers
    temp_list = different_list_of_peers
    # If our_node is in temp_list remove it 
    try:
        temp_list.remove(our_node)
    except ValueError:
        pass
    # Add the new list of peers to list_of_peers
    list_of_peers.extend(temp_list)

    # For testing
    #print(list_of_peers)

# Sends list_of_peers to selected_peer
def send_all_peers(selected_peer):
    selected_peer.send(json.dumps(list_of_peers).encode())
    print("Just sent all peers")

# Adds peers to list_of_peers
def add_to_list_of_peers(peers_to_add):
    # If peers_to_add is empty 
    if not peers_to_add:
        print("peers_to_add is empty")
    # If peers_to_add is not empty
    else:
        # temp_list stores elements in peers_to_add
        temp_list = peers_to_add
        # For each element in temp_list
        for node in temp_list:
            # If the node/element is already in list_of_peers, remove it from temp_list
            if node_is_peer(node):
                temp_list.remove(node)
        # Add the elements in temp_list to list_of_peers
        list_of_peers.extend(temp_list)
        # For testing
        #print(list_of_peers)


# For testing
#new_list_of_peers(different_list_of_peers)
#list_of_peers = ['a', '1', '7']
#peers_to_add = ['6', '3', '7']
#add_to_list_of_peers(peers_to_add)

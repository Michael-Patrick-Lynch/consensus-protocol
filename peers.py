from socket import *
# Maybe we could use json to send objects?
import json

# For testing
#list_of_peers = ['a', '1', '7']
#different_list_of_peers = ['9', '12', '14','a', '18']
list_of_peers = []

# Changes the peers in list_of_peers to the peers in different_list_of_peers
# and ensures that this/our node is included as the first element in the new list of peers 
def new_list_of_peers(different_list_of_peers):
    # Save our node which is the first entry in the list of peers
    our_node = list_of_peers[0]
    # Delete the elements in the list of peers
    list_of_peers.clear()
    # Add our node to the start of the list of peers
    list_of_peers.insert(0, our_node)
    # If our node is in the updated list of peers remove it and carry on if not
    try:
        different_list_of_peers.remove(our_node)
    except ValueError:
        pass
    # Add the updated list of peers to the list of peers
    list_of_peers.extend(different_list_of_peers)

    # For testing
    print(list_of_peers)

# For testing
#new_list_of_peers(different_list_of_peers)


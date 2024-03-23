import socket
import threading
import hashlib
from typing import NamedTuple
from main import send_message

# Protocol details
# Every message is 32-bytes long, to simplify parsing
MESSAGE_HEADER = 32
ENCODING_FORMAT = 'utf-8'
BUFFER_SIZE = 4096  # 4 KB is standard

# Store node port number and IP address as a tuple 
NODE_PORT_NUMBER = 45000 # Within the "private port range"
NODE_IP_ADDRESS = socket.gethostbyname(socket.gethostname())
NODE_ADDRESS = (NODE_IP_ADDRESS, NODE_PORT_NUMBER)

# Application layer commands 
# Note: These are not part of the sockets API, rather these were defined by us
# as part of our protocol
JOIN_NETWORK = "0x0"
LEAVE_NETWORK = "0x1"
UPDATE_LIST_OF_PEERS = "0x2"
REPLACE_LIST_OF_PEERS = "0x3"
SEND_MESSAGE = "0x4"
SEND_FILE = "0x5"
REQUEST_FILE = "0x6"

# Create listening TCP socket using IPv6, binded to the address defined above
node = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
node.bind(NODE_ADDRESS)

# Each running process will maintain a list of its peers on the network
list_of_peers = []

class Node(NamedTuple):
    IP: str
    ID: str

# Generate unique ID's for nodes based on IP address
def generate_node_ID(ip):
    # Convert address to a string
    address_as_string = str(ip)   

    # Encode the string into bytes using utf-8 (hash function need bytes)
    address_as_bytes = address_as_string.encode(ENCODING_FORMAT)

    # Return node_ID as a string of hexidecimal digits
    unique_id = hashlib.sha3_256(address_as_bytes)
    return unique_id.hexdigest()

# Used for testing purposes
def print_all_peers():
    print("List of all peers:")

    for peer in list_of_peers:
        print(f"ID: {peer.ID}, IP Address: {peer.IP}")

# Replaces the peerlist of all nodes with a new peerlist
def replace_peerlist_of_all_nodes_in_network():
    print("Replacing all peerlists")

    threads = []
    # Warning: assumes first element of each nodes peerlist is always itself
    for peer in list_of_peers[1:]:

        # Create threads to send messages to each peer
        IP_address_to_send_message_to = [str(peer.id)]
        threads.append(threading.Thread(target=send_message,\
                args=(UPDATE_LIST_OF_PEERS, IP_address_to_send_message_to)))

    # Start all threads
    [thread.start() for thread in threads]


def add_peer_node_to_our_peerlist(peer_ip_address):
    ID_of_peer = generate_node_ID(peer_ip_address)
    list_of_peers.append(Node(id = ID_of_peer, IP=peer_ip_address))

# Remove a node from our peerlist based on that nodes ID
def remove_node_from_our_peerlist(id_of_node_to_be_removed):
    list_of_peers = [x for x in list_of_peers if x.ID != id_of_node_to_be_removed]
    print(f"Node {id_of_node_to_be_removed} is no longer a peer")


def get_node_id(ip):
    for node in list_of_peers:
        if node.ip == ip:
            return node.ID
    return -1

def get_node_ip(id):
    for node in list_of_peers:
        if node.ID == id:
            return node.IP
    return -1

def node_is_peer(peer):
    return True if peer in [list_of_peers] else False
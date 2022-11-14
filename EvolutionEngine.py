from pythonosc import udp_client
import socket
import random
import time
import Fitness


LOCALHOST = '127.0.0.1'
ENVIRONMENT_RECEIVE_PORT = 2999
ENVIRONMENT_SEND_PORT = 2998
ORGANISM_RECEIVE_PORT = 3001
ORGANISM_SEND_PORT = 3002
SHIFT = 4

environment_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
environment_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
environment_socket.bind((LOCALHOST, ENVIRONMENT_RECEIVE_PORT))

env_udp = udp_client.SimpleUDPClient(LOCALHOST, ENVIRONMENT_SEND_PORT)

organism_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
organism_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
organism_socket.bind((LOCALHOST, ORGANISM_RECEIVE_PORT))

org_udp = udp_client.SimpleUDPClient(LOCALHOST, ORGANISM_SEND_PORT)

def environmental_change_engine():
    max_data = environment_socket.recv(2048).decode('utf-8')
    max_data_stripped = max_data.partition("\x00")[0];
    max_data_list = list(map(int, max_data_stripped.split(' ')))
    print("converted: ", max_data_list, "\n")

    shift_list = max_data_list[SHIFT:] + [0]*SHIFT
    print("shift: ", shift_list, "\n")

    modified_list = [int(val * 1.1) if random.randint(0,1) == 1 else int(val * 0.9) for val in max_data_list] # perhaps make this +/- 5 instead of percent
    print("modified: ", modified_list, "\n")

    env_udp.send_message("/test", modified_list)
    time.sleep(2)

# Receives an organism from Max
# return a nested list of midi value:[[val1,val2,val3...],...], each sub list represents a mutated version organism
def mutation_engine():
    return

def natural_selection_engine(environment):
    organisms = mutation_engine()
    best_fit = organisms[0]
    best_heuristic = Fitness.fitness(environment, organism)
    for organism in organisms:
        heuristic = Fitness.fitness(environment, organism)
        if heuristic < best_heuristic:
            best_heuristic = heuristic
            best_fit = organism
    org_udp.send_message("/bestfit", best_fit)

if __name__ == "__main__":
    while True:
        environmental_change_engine()
        mutation_engine()
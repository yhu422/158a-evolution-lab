from pythonosc import udp_client
import socket
import random
import Fitness

LOCALHOST = '127.0.0.1'
ENVIRONMENT_RECEIVE_PORT = 2999
ENVIRONMENT_SEND_PORT = 2998
ORGANISM_RECEIVE_PORT = 3001
ORGANISM_SEND_PORT = 3002
SHIFT = 4

def change_engine(receive_port=3000, send_port=3000):
    # Opens socket to receive data from Max
    change_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    change_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    change_socket.bind((LOCALHOST, receive_port))
    
    # Retrieves data, organizes it into list
    max_data = change_socket.recv(2048).decode('utf-8')
    max_data_stripped = max_data.partition("\x00")[0];
    max_data_list = list(map(int, max_data_stripped.split(' ')))
    #print("converted: ", max_data_list, "\n")

    # Mutation Engine (Organism) Variant
    if (receive_port == ORGANISM_RECEIVE_PORT):
        print("Mutation (Organism) Engine")
        return mutation_engine(max_data_list)
    else:
        print("Environment Engine")
        # Environment Engine Variant
        # Modifies the single list accordingly
        modified_list = mod_list(max_data_list)
        change_udp = udp_client.SimpleUDPClient(LOCALHOST, send_port)
        change_udp.send_message("/list", modified_list)
        return modified_list

# Receives an organism from Max
# return a nested list of midi value:[[val1,val2,val3...],...], each sub list represents a mutated version organism
def mutation_engine(lst=[]):
    mutated_options_list = []
    for i in range(10):
        mutated_options_list += [mod_list(lst)]
    return mutated_options_list

def mod_list(lst=[]):
    # Shifts list accordingly, so that [0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15] -> [4 5 6 7 8 9 10 11 12 13 14 15 12 13 14 15]
    # And modifies the last 4 elements +/- 3
    shift_list = lst[SHIFT:]
    shift_list = shift_list + [int(val + 3) if random.randint(0,1) == 1 else int(val - 3) for val in shift_list[len(shift_list)-SHIFT:]]
    #print("shift: ", shift_list, "\n")

    # Again modifies the entire list by +/- 5
    modified_list = [int(val + 5) if random.randint(0,1) == 1 else int(val - 5) for val in shift_list]
    #print("modified: ", modified_list, "\n")
    return modified_list

def natural_selection_engine(environment):
    organisms = change_engine(ORGANISM_RECEIVE_PORT, ORGANISM_SEND_PORT)
    best_fit = organisms[0]
    best_heuristic = Fitness.fitness(environment, organism)
    for organism in organisms:
        heuristic = Fitness.fitness(environment, organism)
        if heuristic < best_heuristic:
            best_heuristic = heuristic
            best_fit = organism
    org_udp = udp_client.SimpleUDPClient(LOCALHOST, ORGANISM_SEND_PORT)
    org_udp.send_message("/bestfit", best_fit)

if __name__ == "__main__":
    while True:
        print("TRUE: env_list")
        env_list = change_engine(ENVIRONMENT_RECEIVE_PORT,ENVIRONMENT_SEND_PORT)
        print("TRUE: natural_selection_engine")
        natural_selection_engine(env_list)
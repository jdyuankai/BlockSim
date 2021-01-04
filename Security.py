import random
from InputsConfig import InputsConfig as p
from Event import Event, Queue
from Models.Network import DBDCNetwork

class Security:

    node_attack_status_list = [False for _ in range(p.Nn)]

    def create_attack_event(node_num, event_time):
        event_type = "attack_node"
        event = Event(event_type, node_num, event_time, None) 
        Queue.add_event(event)

    def generate_initial_events():
        attack_node_nums = p.Nn // 10
        time_interval = p.simTime // attack_node_nums
        if p.BoardcastType == "Gossip":
            attack_node_list = random.sample(range(p.Nn), attack_node_nums)
        elif p.BoardcastType == "DBDC":
            attack_node_list = random.sample(set(range(p.Nn)) - set(DBDCNetwork.node_repre), attack_node_nums)

        attack_timestamp_list = range(p.simTime)[::time_interval]

        for index, node_num in enumerate(attack_node_list):
            Security.create_attack_event(node_num, attack_timestamp_list[index])

    def handle_attack_event(event):
        Security.node_attack_status_list[event.node] = True

    def get_node_attack_status(node_num):
        return Security.node_attack_status_list[node_num]

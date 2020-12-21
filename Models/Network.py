import random
from clustering import dbdc
from InputsConfig import InputsConfig as p

class Network:
    ROUND_TIME = 1.0
    CHOICE_NODE = 30
    
    nodes, _, delays = dbdc._generate_nodes(p.Nn, 10) 
    delay = [[__/1000 for __ in _] for _ in delays]
    cluster_labels, label_repre = dbdc.decide_cluster(nodes)

    # Delay for propagating blocks in the network
    def block_prop_delay():
    	return random.expovariate(1/p.Bdelay)

    # Delay for propagating transactions in the network
    def tx_prop_delay():
    	return random.expovariate(1/p.Tdelay)

    def select_node_and_gen_delay(block, event_node):
        pass


class GossipNetwork(Network):

    def calc_node_adj(cluster_labels, label_repre):
        node_lens = len(cluster_labels)
        set_lens = len(set(cluster_labels))
        mid_result = [[] for _ in range(set_lens)]
        result = [[] for _ in range(node_lens)]

        repre_result = []
        for key in label_repre:
            repre_result.append(label_repre[key])
        
        for key in label_repre:
            result[label_repre[key]] += repre_result
            result[label_repre[key]].remove(label_repre[key])

        for i, c in enumerate(cluster_labels):
            mid_result[c].append(i)
        
        for i, c in enumerate(cluster_labels):
            result[i] += mid_result[c]
            result[i].remove(i)

        return result
    
    node_adj = calc_node_adj(Network.cluster_labels, Network.label_repre)

    def select_node_and_gen_delay(block, event_node):
        node_cache = GossipNetwork.node_adj[event_node][:]
        delay_time = 0
        result = []

        while len(node_cache) != 0:
            if len(node_cache) >= Network.CHOICE_NODE: 
                round_node_cache = random.sample(node_cache, Network.CHOICE_NODE)
            else:
                round_node_cache = node_cache[:]

            for node in round_node_cache:
                if node != block.miner and block.broadcast_status[node] == False:
                    block_delay = random.expovariate(1/Network.delay[block.miner][node])
                    result.append((p.NODES[node], block_delay + delay_time))
                node_cache.remove(node)
            
            delay_time += Network.ROUND_TIME
        return result

class DBDCNetwork(Network):

    def calc_node_adj_and_repre(cluster_labels, label_repre):
        node_lens = len(cluster_labels)
        set_lens = len(set(cluster_labels))
        mid_result = [[] for _ in range(set_lens)]
        result = [[] for _ in range(node_lens)]

        repre_result = []
        for key in label_repre:
            repre_result.append(label_repre[key])

        for key in label_repre:
            result[label_repre[key]] += repre_result
            result[label_repre[key]].remove(label_repre[key])

        for i, c in enumerate(cluster_labels):
            mid_result[c].append(i)
        
        for i, c in enumerate(cluster_labels):
            result[i] += mid_result[c]
            result[i].remove(i)

        return result, repre_result
    
    node_adj, node_repre = calc_node_adj_and_repre(Network.cluster_labels, Network.label_repre)

    def select_node_and_gen_delay(block, event_node):
        
        delay_time = 0
        result = []

        def broadcast(block, event_node, delay_time, type, result):
            node_cache = DBDCNetwork.node_adj[event_node][:]
            node_repre = DBDCNetwork.node_repre[:]

            broadcast_next = []

            if type == "g=>g&r":
                broadcast_to = set(node_cache) - set(node_repre)
                broadcast_to.add(Network.label_repre[Network.cluster_labels[event_node]])
                broadcast_next_type = "r=>r"
            elif type == "r=>g&r":
                broadcast_to = node_cache
                broadcast_next_type = "r=>g"
            elif type == "r=>r":
                broadcast_to = set(node_repre) - set([event_node])
                broadcast_next_type = "r=>g"
            elif type == "r=>g":
                broadcast_to = set(node_cache) - set(node_repre)
                broadcast_next_type = None
            else:
                return
            
            for node in broadcast_to:
                if node != block.miner and block.broadcast_status[node] == False:
                    block_delay = random.expovariate(1/Network.delay[event_node][node])
                    result.append((p.NODES[node], block_delay + delay_time))
                    if node in DBDCNetwork.node_repre:
                        broadcast_next.append((node, block_delay + delay_time))

            for node, node_delay_time in broadcast_next:
                broadcast(block, node, node_delay_time, broadcast_next_type, result)

        if event_node in DBDCNetwork.node_repre:
            broadcast(block, event_node, delay_time, "r=>g&r", result)
        else:
            broadcast(block, event_node, delay_time, "g=>g&r", result)

        return result


if p.BoardcastType == "Gossip":
    network = GossipNetwork
elif p.BoardcastType == "DBDC":
    network = DBDCNetwork
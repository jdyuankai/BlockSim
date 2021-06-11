from clustering import dbdc
from InputsConfig import InputsConfig as p

class DataProvider():
    def generate_nodes():
        pass

    def decide_cluster(nodes):
        pass

class DataProvider4Gossip(DataProvider):
    def generate_nodes():
        return dbdc._generate_nodes(p.Nn * 10, 1)

    def decide_cluster(nodes):
        return dbdc.decide_cluster(nodes)


class DataProvider4Dbdc(DataProvider):
    def generate_nodes():
        return dbdc._generate_nodes(p.Nn, 10)

    def decide_cluster(nodes):
        return dbdc.decide_cluster(nodes)


if p.BoardcastType == "Gossip":
    dataProvider = DataProvider4Gossip
elif p.BoardcastType == "DBDC":
    dataProvider = DataProvider4Dbdc
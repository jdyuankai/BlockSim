from InputsConfig import InputsConfig as p
from Output import Output

class Block(object):
    
    """ Defines the base Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    """

    def __init__(self,
	 depth=0,
	 id=0,
	 previous=-1,
	 timestamp=0,
	 miner=None,
	 transactions=[],
	 size=1.0):

        self.depth = depth
        self.id = id
        self.previous = previous
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions or []
        self.size = size
        self.broadcast_status = [False for _ in range(p.Nn)]
        self.broadcast_counter = 0
        if self.miner is not None:
            self.block_receive(miner, timestamp)

    def block_receive(self, recipient_id, timestamp):
        if self.broadcast_status[recipient_id] == False:
            self.broadcast_status[recipient_id] = True
            self.broadcast_counter += 1
            
            ratio = self.broadcast_counter / p.Nn
            Output.add(timestamp, self.id, recipient_id, self.broadcast_counter, ratio)
            # if ratio == 0.1:
            #     print("Block {id} is already broadcast 10% of nodes at the time of {timestamp}".format(id=self.id, timestamp=timestamp))
            # elif ratio == 0.5:
            #     print("Block {id} is already broadcast 50% of nodes at the time of {timestamp}".format(id=self.id, timestamp=timestamp))
            # elif ratio == 1.0:
            #     print("Block {id} is already broadcast 100% of nodes at the time of {timestamp}".format(id=self.id, timestamp=timestamp))


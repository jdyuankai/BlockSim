import random
from Scheduler import Scheduler
from InputsConfig import InputsConfig as p
from Models.Trias.Node import Node
from Statistics import Statistics
from Models.Transaction import LightTransaction as LT, FullTransaction as FT
from Models.Network import network
from Models.Trias.Consensus import Consensus as c
from Models.BlockCommit import BlockCommit as BaseBlockCommit
from Security import Security

class BlockCommit(BaseBlockCommit):

    # Handling and running Events
    def handle_event(event):
        if p.attack and Security.get_node_attack_status(event.node):
            return

        if event.type == "create_block":
            BlockCommit.generate_block(event)
        elif event.type == "receive_block":
            BlockCommit.receive_block(event)
        elif event.type == "attack_node":
            Security.handle_attack_event(event)

    # Block Creation Event
    def generate_block (event):
        miner = p.NODES[event.block.miner]
        minerId = miner.id
        eventTime = event.time
        blockPrev = event.block.previous

        if blockPrev == miner.last_block().id:
            Statistics.totalBlocks += 1 # count # of total blocks created!
            if p.hasTrans:
                if p.Ttechnique == "Light": blockTrans,blockSize = LT.execute_transactions()
                elif p.Ttechnique == "Full": blockTrans,blockSize = FT.execute_transactions(miner,eventTime)

                event.block.transactions = blockTrans
                event.block.usedgas= blockSize

            miner.blockchain.append(event.block)

            if p.hasTrans and p.Ttechnique == "Light":LT.create_transactions() # generate transactions

            BlockCommit.propagate_block(event.block, miner.id, eventTime)
            BlockCommit.generate_next_block(miner,eventTime)# Start mining or working on the next block

    # Block Receiving Event
    def receive_block (event):

        if event.block.broadcast_status[event.node] == True:
            return

        miner = p.NODES[event.block.miner]
        minerId = miner.id
        currentTime = event.time
        blockPrev = event.block.previous # previous block id


        node = p.NODES[event.node] # recipint
        lastBlockId= node.last_block().id # the id of last block

        #### case 1: the received block is built on top of the last block according to the recipient's blockchain ####
        if blockPrev == lastBlockId:
            node.blockchain.append(event.block) # append the block to local blockchain
            if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node, event.block)
            BlockCommit.generate_next_block(node,currentTime)# Start mining or working on the next block

         #### case 2: the received block is  not built on top of the last block ####
        else:
            depth = event.block.depth + 1
            if (depth > len(node.blockchain)):
                BlockCommit.update_local_blockchain(node,miner,depth)
                BlockCommit.generate_next_block(node,currentTime)# Start mining or working on the next block

            if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,event.block) # not sure yet.
        
        event.block.block_receive(event.node, currentTime)
        BlockCommit.propagate_block(event.block, event.node, currentTime)

    # Upon generating or receiving a block, the miner start working on the next block as in POW
    def generate_next_block(node,currentTime):
	    if node.hashPower > 0:
                 blockTime = currentTime + c.Protocol(node) # time when miner x generate the next block
                 Scheduler.create_block_event(node,blockTime)

    def generate_initial_events():
            currentTime=0
            for node in p.NODES:
            	BlockCommit.generate_next_block(node,currentTime)

    def propagate_block(block, event_node, current_time):
        for recipient, delay in network.select_node_and_gen_delay(block, event_node):
            Scheduler.receive_block_event(recipient, block, current_time + delay)

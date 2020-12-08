from InputsConfig import InputsConfig as p
import random
from Models.Block import Block
from Event import Event, Queue

if p.model==2:from Models.Ethereum.Block import Block
else: from Models.Block import Block

class Scheduler:

    # Schedule a block creation event for a miner and add it to the event list
    def create_block_event(miner,eventTime):
        eventType = "create_block"
        if eventTime <= p.simTime:
                # prepare attributes for the event
                block= Block(
                    depth= len(miner.blockchain),
                    id= random.randrange(100000000000),
                    previous= miner.last_block().id,
                    timestamp= eventTime,
                    miner= miner.id,
                )

                event = Event(eventType,block.miner,eventTime,block) # create the event
                Queue.add_event(event) # add the event to the queue

    # Schedule a block receiving event for a node and add it to the event list
    def receive_block_event(recipient, block, event_time):
        if event_time <= p.simTime:
                e = Event("receive_block", recipient.id, event_time, block)
                Queue.add_event(e)

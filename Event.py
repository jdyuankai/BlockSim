import operator
import heapq
from InputsConfig import InputsConfig as p

class Event(object):

    """ Defines the Evevnt.

        :param str type: the event type (block creation or block reception)
        :param int node: the id of the node that the event belongs to
        :param float time: the simualtion time in which the event will be executed at
        :param obj block: the event content "block" to be generated or received
    """
    def __init__(self,type, node, time, block):
        self.type = type
        self.node = node
        self.time = time
        self.block = block
    
    def __lt__(self, e):
        if self.time < e.time:
            return True
        else:
            return False

class Queue:
    event_list=[] # this is where future events will be stored
    def add_event(event):
        # print(event.type, event.node, event.time, event.block)
        heapq.heappush(Queue.event_list, (event.time, event))
    def pop_event():
        _, event = heapq.heappop(Queue.event_list)
        return event
    def size():
        return len(Queue.event_list)
    def isEmpty():
        return len(Queue.event_list) == 0
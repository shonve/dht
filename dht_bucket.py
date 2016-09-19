from dht_node import node
from define import BUCKET_MAX_NUM
from time import time
from utils import BucketFull


class bucket:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.nodes = []
        self.access_time = time()

    def bucket_len(self):
        return len(self.nodes)

    def add_node(self, node):
        if len(node.node_id) != 20:
            return

        if self.bucket_len() < BUCKET_MAX_NUM:
            if node not in self.nodes:
                self.nodes.append(node)
            self.access_time = time()
        else:
            raise BucketFull

    def node_in_range(self, node):
        return (self.min <= node.node_id) and (node.node_id < self.max)
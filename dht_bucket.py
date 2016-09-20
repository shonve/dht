from dht_node import Node
from define import BUCKET_MAX_NUM

from utils import BucketFull


class Bucket:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.nodes = {}


    def bucket_len(self):
        return len(self.nodes)

    def add_node(self, node):
        if len(node.node_id) != 20:
            return

        if self.bucket_len() < BUCKET_MAX_NUM:
            if node.node_id not in self.nodes:
                self.nodes[node.node_id] = node
        else:
            raise BucketFull

    def node_in_range(self, node):
        return (self.min <= node.node_id) and (node.node_id < self.max)

    def node_in_range_by_id(self, node_id):
        return (self.min <= node_id) and (node_id < self.max)
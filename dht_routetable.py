from dht_node import Node
from dht_bucket import Bucket
from define import FIND_NODE_MAX_NUM
from utils import BucketFull, hash_to_long
from threading import Lock

class R_table:
    def __init__(self, node):
        self.node = node  # your own node
        self.bucktes = [Bucket(0, 2 ** 160)]
        self.lock = Lock()

    def index_of_bucket(self, node):
        for index, bucket in enumerate(self.bucktes):
            if bucket.node_in_range(node):
                return index
        return index

    def index_of_bucket_by_id(self, node_id):
        for index, bucket in enumerate(self.bucktes):
            if bucket.node_in_range_by_id(node_id):
                return index
        return index

    def add_node(self, node):
        if node.node_id == self.node.node_id:
            return
        index = self.index_of_bucket(node)
        bucket = self.bucktes[index]

        try:
            bucket.add_node(node)
        except BucketFull:
            if not bucket.node_in_range(node):
                return
            with self.lock:
                self.split_bucket(index)
                self.add_node(node)

    def split_bucket(self, index):
        old = self.bucktes[index]
        mid = (old.max - old.min) / 2 + old.min
        with self.lock:
            new = Bucket[mid, old.max]
            old.max = mid
            self.bucktes.insert(index + 1, new)
            for node in old:
                if new.node_in_range(node):
                    new.add_node(node)
            for node in new:
                old.remove(node)

    def find_close_node(self, target):
        # target is a node
        nodes = []
        if len(self.bucktes) == 0:
            return
        index = self.index_of_bucket(target)
        nodes = self.bucktes[index].nodes
        min = index - 1
        max = index + 1
        with self.lock:
            while (len(nodes) < FIND_NODE_MAX_NUM) and (min >= 0 or max < len(self.bucktes)):
                if min >= 0:
                    nodes.extend(self.bucktes[min].nodes)
                if max < len(self.bucktes):
                    nodes.extend(self.bucktes[max].nodes)
                min -= 1
                max += 1

        num = hash_to_long(target.node_id)
        nodes.sort(lambda node_a, node_b, num=num: cmp(num ^ hash_to_long(node_a.node_id),
                                                      num ^ hash_to_long(node_b.node_id)))
        return nodes[:FIND_NODE_MAX_NUM]

    def find_node_by_id(self, id):
        index = self.index_of_bucket_by_id(id)
        nodes = self.bucktes[index].nodes
        with self.lock:
            if id in nodes:
                return nodes[id]
        return None

    def find_node_by_tid(self, tid):
        for bucket in self.bucktes:
            for node_id in bucket.nodes:
                if tid in bucket.nodes[node_id].trans:
                    return bucket.nodes[node_id]






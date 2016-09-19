from dht_node import node

class bucket:
    def __init__(self):
        self.nodes = []

    def bucket_len(self):
        return len(self.nodes)

    def add_node(self):
        self.nodes.append()
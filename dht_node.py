class node:
    def __init__(self, node_id, node_ip, node_port):
        self.node_id = node_id
        self.node_ip = node_ip
        self.node_port = node_port

    def __eq__(self, other):
        return self.node_id == other.node_id

    def __ne__(self, other):
        return self.node_id != other.node_id



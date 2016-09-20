import threading
from time import time

class Node:
    def __init__(self, node_id, node_ip, node_port):
        self.node_id = node_id
        self.node_ip = node_ip
        self.node_port = node_port
        self.trans = {}
        self.access_time = time()
        self.lock = threading.Lock()

    def __eq__(self, other):

        return self.node_id == other.node_id

    def __ne__(self, other):
        return self.node_id != other.node_id

    def delete_tran(self, tid):
        with self.lock:
            del self.trans[tid]

    def update_access(self):
        self.access_time = time()



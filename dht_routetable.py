from dht_node import node
from dht_bucket import bucket
import define
class r_table:
    def __init__(self):
        self.bucktes = []

    def add_node(self):
        self.bucktes
        if bucket.bucket_len()>=define.BUCKET_MAX_NUM:
            self.split_bucket()
        else:
            self.buckte.

    def split_bucket(self):

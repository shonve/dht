class BucketFull(Exception):
    pass

def hash_to_long(node_id):
    assert len(node_id) == 20
    return long(node_id.encode('hex'), 16)

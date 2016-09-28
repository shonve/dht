import struct
from hashlib import sha1
from random import randint
from define import NODE_LENGTH


class BucketFull(Exception):
    pass


def hash_to_long(node_id):
    assert len(node_id) == 20
    return long(node_id.encode('hex'), 16)


def random_node_id():
    h = sha1()
    h.update("".join(chr(randint(0, 255)) for _ in xrange(NODE_LENGTH)))
    return h.digest()


def dottedQuadToNum(ip):
    """ Convert decimal dotted quad string to long integer """
    hexn = ''.join(["%02X" % long(i) for i in ip.split('.')])
    return long(hexn, 16)


def numToDottedQuad(n):
    """ Convert long int to dotted quad string """
    d = 256 * 256 * 256
    q = []
    while d > 0:
        m, n = divmod(n, d)
        q.append(str(m))
        d /= 256
    return '.'.join(q)


def decode_nodes(nodes):
    """ Decode node_info into a list of id, connect_info """
    nrnodes = len(nodes) / 26
    nodes = struct.unpack("!" + "20sIH" * nrnodes, nodes)
    for i in xrange(nrnodes):
        node_id, ip, port = nodes[i * 3], numToDottedQuad(nodes[i * 3 + 1]), nodes[i * 3 + 2]
        yield node_id, ip, port


def encode_nodes(nodes):
    """ Encode a list of (id, connect_info) pairs into a node_info """
    n = []
    for node in nodes:
        n.extend([node[0], dottedQuadToNum(node[1].host), node[1].port])
        return struct.pack("!" + "20sIH" * len(nodes), *n)




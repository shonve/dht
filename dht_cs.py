from hashlib import sha1
from threading import Thread, Timer
from time import time
from utils import random_node_id
from bencode import bencode, bdecode, BTFailure
from dht_node import Node
from dht_routetable import R_table
import SocketServer
from threading import Lock, Thread


class DHTRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        if self.server.dht.ip == self.client_address[0]:
            return

        req = self.request[0].strip()

        try:
            msg = bdecode(req)
            msg_type = msg['y']

            if msg_type == 'r':
                self.handle_response(msg)
            elif msg_type == 'q':
                self.handle_query(msg)
            elif msg_type == 'e':
                self.handle_error(msg)
            else:
                print 'no such key: %s'%msg_type
        except BTFailure:
            print 'fail to bdecode'
            pass

    def handle_response(self, msg):
        trans_id = msg['t']
        args = msg['r']
        node_id = msg['id']

        client_ip, client_port = self.client_address

        node = self.server.dht.rt.find_node_by_id(node_id)
        if not node:
            node = self.server.dht.rt.find_node_by_tid(trans_id)
            if not node:
                return

        if trans_id in node.trans:
            try:
                tran = node.trans[trans_id]
                node.delete_tran(trans_id)
            except:
                return
        else:
            return

        try:
            t_name = tran['name']
        except:
            return

        if t_name == 'find_node':
            node.update_access()
            if 'node' in args:
                print args['nodes']








class DHTServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    def __init__(self, address, handle):
        SocketServer.UDPServer.__init__(self, address, handle)
        self.send_lock = Lock()


class DHT(object):
    def __init__(self, host, port):
        self.ip = host
        self.port = port
        self.id = random_node_id()
        self.node = Node(self.id, unicode(host), port)
        self.rt = R_table(self.node)

        self.server = DHTServer((self.node.node_ip, self.node.node_port), DHTRequestHandler)
        self.server.dht = self


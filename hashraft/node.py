from .rpc.ServerRPC import ServerRPC

class Node (ServerRPC):
    def __init__ (self, ip, port, name, nodes):
        super ().__init__ (ip, port, 1024)
        self.name = name
        self.nodes = nodes

    def ping (self):
        return 100

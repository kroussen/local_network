class Server:
    _id_counter = 1

    def __init__(self):
        self.ip = Server._id_counter
        Server._id_counter += 1

        self.buffer = []
        self.router = None

    def send_data(self, data):
        if self.router:
            self.router.buffer.append(data)

    def get_data(self):
        received_data = self.buffer[:]
        self.buffer.clear()
        return received_data

    def get_ip(self):
        return self.ip

    def connect_router(self, obj_router):
        self.router = obj_router


class Router:
    def __init__(self):
        self.buffer = []
        self.servers = {}

    def link(self, server):
        self.servers[server.get_ip()] = server
        server.connect_router(self)

    def unlink(self, server):
        if server.get_ip() in self.servers:
            del self.servers[server.get_ip()]
            server.connect_router(None)

    def send_data(self):
        for data in self.buffer:
            if self.servers.get(data.ip):
                self.servers[data.ip].buffer.append(data)
        self.buffer.clear()


class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip

import socket, pickle
import sqlite3


class MySocket(socket.socket):
    def __init__(self, type, addr):
        super().__init__(socket.AF_INET,
            socket.SOCK_DGRAM if type == "UDP"
            else socket.SOCK_STREAM)

        if not len(addr[0]):
            self.bind(addr)
            self.listen()
            self.conn = None
            self.client = None
        else:
            self.connect(addr)
            self.conn = self

    def accept(self):
        self.conn, self.client = super().accept()
        return self.conn, self.client

    def close(self):
        self.conn, self.client = None, None
        super().close()

    def send_msg(self, msg):
        self.conn.sendall(msg.encode("utf-8"))

    def send_obj(self, obj):
        self.conn.sendall(pickle.dumps(obj))

    def recvall(self):
        return MySocket.recvall(self.conn)

    def recvall(conn):
        datos = b""
        buff_size = 1024

        conn.setblocking(True)
        try:
            while True:
                datos += conn.recv(buff_size)
                conn.setblocking(False)
        except socket.error: pass
        conn.setblocking(True)

        return datos

    def recv_msg(self):
        return MySocket.recvall(self.conn).decode("utf-8")

    def recv_obj(self):
        return pickle.loads(MySocket.recvall(self.conn))


def rundb(dbfile, query, parameters=()):
    with sqlite3.connect(dbfile) as db:
        cur = db.cursor()
        res = cur.execute(query, parameters)
        db.commit()
    return res
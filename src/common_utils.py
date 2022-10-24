import socket, pickle, struct
import sqlite3


class MySocket(socket.socket):
    def __init__(self, type, addr):
        super().__init__(socket.AF_INET,
            socket.SOCK_DGRAM if type == "UDP"
            else socket.SOCK_STREAM)

        if not len(addr[0]):
            self.bind(addr)
            self.listen()
            self.conn = {}
        else:
            self.connect(addr)
            self.conn = {"None":self}

    def accept(self):
        conn, client = super().accept()
        self.conn["None"] = conn
        self.conn[client] = conn
        return conn, client

    def close(self):
        self.conn, self.client = None, None
        super().close()

    def pack(data):
        packet_len = struct.pack("!I", len(data))
        return packet_len + data

    def send_msg(self, msg, client="None"):
        self.conn[client].sendall(MySocket.pack(msg.encode("utf-8")))

    def send_obj(self, obj, client="None"):
        self.conn[client].sendall(MySocket.pack(pickle.dumps(obj)))

    def recv_confirmed(conn, buf_len):
        buf = b""
        while len(buf) < buf_len:
            buf += conn.recv(buf_len-len(buf))
        return buf

    def recvall(conn):
        buf_len = struct.unpack("!I", MySocket.recv_confirmed(conn,4))[0]
        return MySocket.recv_confirmed(conn, buf_len)

    def recv_msg(self, client="None"):
        return MySocket.recvall(self.conn[client]).decode("utf-8")

    def recv_obj(self, client="None"):
        return pickle.loads(MySocket.recvall(self.conn[client]))


def rundb(dbfile, query, parameters=()):
    with sqlite3.connect(dbfile) as db:
        cur = db.cursor()
        res = cur.execute(query, parameters)
        db.commit()
    return res
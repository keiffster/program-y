import socket
import sys

MSGLEN = 1024

class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                return
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                return b''.join(chunks)
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)


if __name__ == '__main__':

    host = sys.argv[1]
    port = int(sys.argv[2])
    question = '{"userid": "1234567890", "question": "%s}"}' % sys.argv[3]

    sock = MySocket()

    sock.connect(host, port)

    sock.mysend(bytearray(question, encoding ='utf-8'))

    result = sock.myreceive()
    print(result.decode('utf-8'))

import socket

class FTPClient:
    def __init__(self, host, port=21, timeout=3.0):
        self.host, self.port, self.timeout = host, port, timeout
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((self.host,self.port),timeout=self.timeout)
        self.sock.settimeout(self.timeout)
        return self._recv()

    def command(self, cmd):
        self.sock.sendall((cmd.rstrip()+"\r\n").encode())
        return self._recv()

    def _recv(self):
        chunks=[]
        while True:
            try: data=self.sock.recv(4096)
            except socket.timeout: break
            if not data: break
            chunks.append(data)
            text=b"".join(chunks).decode(errors="replace")
            lines=text.splitlines()
            if lines and len(lines[-1])>=4 and lines[-1][:3].isdigit() and lines[-1][3]==" ":
                break
            if sum(map(len,chunks))>=65536: break
        return b"".join(chunks).decode(errors="replace").strip()

    def close(self):
        if self.sock: self.sock.close()

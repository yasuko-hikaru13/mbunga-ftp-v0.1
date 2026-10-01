import socket, re

class FTPClient:
    def __init__(self, host, port=21, timeout=3.0):
        self.host, self.port, self.timeout = host, port, timeout
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((self.host,self.port),timeout=self.timeout)
        self.sock.settimeout(self.timeout)
        return self._recv()

    def login(self, user="anonymous", passwd="anonymous@"):
        r = self.command(f"USER {user}")
        if r.startswith("331"):
            r = self.command(f"PASS {passwd}")
        return r

    def command(self, cmd):
        self.sock.sendall((cmd.rstrip()+"\r\n").encode())
        return self._recv()

    def pasv(self):
        """Enter passive mode; returns (ip, port) for the data connection."""
        resp = self.command("PASV")
        m = re.search(r"\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)", resp)
        if not m:
            raise RuntimeError(f"Bad PASV response: {resp}")
        g = [int(x) for x in m.groups()]
        ip = ".".join(map(str, g[:4]))
        port = g[4]*256 + g[5]
        return ip, port

    def stor(self, name, data):
        """Upload bytes as `name` via STOR in passive mode."""
        ip, port = self.pasv()
        dsock = socket.create_connection((ip, port), timeout=self.timeout)
        resp = self.command(f"STOR {name}")
        if not resp.startswith(("150", "125")):
            dsock.close()
            raise RuntimeError(f"STOR refused: {resp}")
        dsock.sendall(data)
        dsock.close()
        return self._recv()  # 226 transfer complete

    def pwd(self):
        resp = self.command("PWD")
        m = re.search(r'"([^"]+)"', resp)
        return m.group(1) if m else "/"

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
        if self.sock:
            try: self.sock.close()
            except OSError: pass

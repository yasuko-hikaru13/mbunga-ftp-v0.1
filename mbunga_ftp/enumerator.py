from .client import FTPClient
from .fingerprint import fingerprint

def enumerate_ftp(host,port=21,timeout=3.0):
    ftp=FTPClient(host,port,timeout)
    try:
        banner=ftp.connect()
        fp=fingerprint(banner)
        responses={}
        for cmd in ("SYST","FEAT","HELP"):
            try: responses[cmd]=ftp.command(cmd)
            except OSError as e: responses[cmd]=f"ERROR: {e}"
        return {"host":host,"port":port,"banner":banner,**fp,
                "syst":responses["SYST"],"feat":responses["FEAT"],"help":responses["HELP"]}
    finally:
        ftp.close()

import re

def fingerprint(banner):
    patterns=[(r"(ProFTPD)\\s+([0-9][\\w.\\-]+)","ProFTPD"),
              (r"(vsFTPd)\\s+([0-9][\\w.\\-]+)","vsFTPd")]
    for pattern,name in patterns:
        m=re.search(pattern,banner,re.I)
        if m: return {"product":name,"version":m.group(2)}
    return {"product":"Unknown FTP server","version":None}

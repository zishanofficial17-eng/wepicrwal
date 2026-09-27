#!/usr/bin/env python3
import argparse
import datetime
import html
import os
import re
import socket
import sys
import threading
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[!] Missing dependencies. Run: pip install requests beautifulsoup4")
    sys.exit(1)

requests.packages.urllib3.disable_warnings()


class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_banner():
    banner = r"""
                                     ███                                               ████ 
                                    ░░░                                               ░░███ 
 █████ ███ █████  ██████  ████████  ████   ██████  ████████  █████ ███ █████  ██████   ░███ 
░░███ ░███░░███  ███░░███░░███░░███░░███  ███░░███░░███░░███░░███ ░███░░███  ░░░░░███  ░███ 
 ░███ ░███ ░███ ░███████  ░███ ░███ ░███ ░███ ░░░  ░███ ░░░  ░███ ░███ ░███   ███████  ░███ 
 ░░███████████  ░███░░░   ░███ ░███ ░███ ░███  ███ ░███      ░░███████████   ███░░███  ░███ 
  ░░████░████   ░░██████  ░███████  █████░░██████  █████      ░░████░████   ░░████████ █████
   ░░░░ ░░░░     ░░░░░░   ░███░░░  ░░░░░  ░░░░░░  ░░░░░        ░░░░ ░░░░     ░░░░░░░░ ░░░░░ 
                          ░███                                                              
                          █████       wepicrwal - Web Vuln Scanner               
                         ░░░░░        
    -----------------------------------------------------
          Developed by: Md Zishan Raza
    -----------------------------------------------------
"""
    print(C.CYAN + banner + C.END)


def authorization_gate(target):
    print(C.YELLOW + C.BOLD + "\n[LEGAL AUTHORIZATION REQUIRED]" + C.END)
    print(C.YELLOW + (
        "Scanning ports / testing for vulnerabilities on a system without\n"
        "explicit written permission from its owner is ILLEGAL in most\n"
        "jurisdictions (IT Act 2000 / CFAA / Computer Misuse Act, etc.)\n"
        "This tool must only be used on systems you OWN or are AUTHORIZED\n"
        "in writing to test (e.g. your own lab, a CTF box, or a client with\n"
        "a signed pentest agreement).\n"
    ) + C.END)
    print(f"Target entered: {C.BOLD}{target}{C.END}\n")

    typed_target = input("Re-type the exact target domain/IP to confirm: ").strip()
    if typed_target != target:
        print(C.RED + "[!] Target mismatch. Aborting for safety." + C.END)
        sys.exit(1)

    consent = input(
        'Type exactly: "I CONFIRM I HAVE PERMISSION" to proceed: '
    ).strip()
    if consent != "I CONFIRM I HAVE PERMISSION":
        print(C.RED + "[!] Authorization not confirmed. Aborting." + C.END)
        sys.exit(1)

    print(C.GREEN + "[+] Authorization confirmed. Proceeding with scan...\n" + C.END)


PORT_INFO = {
    21:   ("FTP",         "unsafe",   "Unencrypted file transfer; credentials & data sent in plaintext."),
    22:   ("SSH",         "review",   "Encrypted shell access; ensure strong keys and restrict public IP."),
    23:   ("Telnet",      "unsafe",   "Completely unencrypted remote login - credentials can be sniffed in plaintext."),
    25:   ("SMTP",        "moderate", "Mail relay; if misconfigured can be abused as an open relay for spam/phishing."),
    53:   ("DNS",         "moderate", "Can be abused for DNS amplification/DDoS or zone transfer info leaks if misconfigured."),
    80:   ("HTTP",        "moderate", "Standard web traffic but unencrypted; use HTTPS instead."),
    110:  ("POP3",        "unsafe",   "Unencrypted email retrieval - credentials sent in plaintext."),
    111:  ("RPCbind",     "unsafe",   "Exposes RPC services, often used for enumeration and further exploitation."),
    135:  ("MSRPC",       "unsafe",   "Windows RPC endpoint mapper - historically targeted by worms and remote exploits."),
    139:  ("NetBIOS-SSN", "unsafe",   "Legacy Windows file sharing; prone to enumeration and relay attacks."),
    143:  ("IMAP",        "unsafe",   "Unencrypted email access - credentials sent in plaintext."),
    443:  ("HTTPS",       "safe",     "Encrypted web traffic (TLS/SSL)."),
    445:  ("SMB",         "unsafe",   "File sharing service; historically exploited by ransomware (e.g. EternalBlue/WannaCry)."),
    993:  ("IMAPS",       "safe",     "Encrypted IMAP. Safe if TLS config is current."),
    995:  ("POP3S",       "safe",     "Encrypted POP3. Safe if TLS config is current."),
    1433: ("MSSQL",       "unsafe",   "Database exposed to public internet; brute-force & data leak risk."),
    3306: ("MySQL",       "unsafe",   "Database exposed to public internet; brute-force & data leak risk."),
    3389: ("RDP",         "critical", "Remote desktop exposed; high risk of brute-force and ransomware."),
    5900: ("VNC",         "unsafe",   "Remote desktop, often with weak/no authentication by default."),
    6379: ("Redis",       "critical", "Frequently deployed with no authentication - can lead to full server compromise."),
    8080: ("HTTP-Alt",    "moderate", "Alternate web/admin interface; unencrypted, often left with default configs."),
    8443: ("HTTPS-Alt",   "moderate", "Alternate encrypted web port; verify TLS config."),
    27017:("MongoDB",     "critical", "Frequently deployed with no authentication - direct database exposure risk."),
}

UDP_PORT_INFO = {
    53:    ("DNS",       "moderate", "Open resolver risk; can be abused for DNS amplification attacks."),
    67:    ("DHCP",      "moderate", "DHCP service exposed; potential rogue DHCP server risk."),
    69:    ("TFTP",      "unsafe",   "Trivial FTP - no authentication, often used for data exfiltration."),
    123:   ("NTP",       "unsafe",   "Monlist query abuse; vulnerable to NTP amplification DDoS."),
    161:   ("SNMP",      "unsafe",   "Information disclosure; system metrics/network data exposed."),
    500:   ("IKE",       "moderate", "VPN key exchange; misconfig can leak VPN details."),
    1900:  ("SSDP",      "moderate", "UPnP discovery; used in SSDP amplification DDoS."),
    4500:  ("IPSEC-NAT", "moderate", "NAT-T for VPN; review exposure."),
    5353:  ("mDNS",      "moderate", "Multicast DNS; information disclosure on local networks."),
    11211: ("Memcached", "critical", "High amplification DDoS risk (up to 50,000x) & unauth memory dump."),
}


def scan_port(target_ip, port, results, timeout=1.0, proto="tcp"):
    try:
        if proto == "tcp":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                if s.connect_ex((target_ip, port)) == 0:
                    results[port] = "open"
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                try:
                    s.sendto(b"\x00", (target_ip, port))
                    s.recvfrom(1024)
                    results[port] = "open"
                except socket.timeout:
                    pass
                except socket.error:
                    pass
    except socket.error:
        pass


def print_port_line(port, service, status, caption, proto="tcp"):
    if status == "critical":
        tag = C.RED + C.BOLD + "CRITICAL" + C.END
    elif status == "unsafe":
        tag = C.RED + "UNSAFE" + C.END
    elif status == "safe":
        tag = C.GREEN + "SAFE" + C.END
    elif status == "review":
        tag = C.YELLOW + "SAFE/REVIEW" + C.END
    else:
        tag = C.YELLOW + "MODERATE" + C.END

    suffix = "/udp" if proto == "udp" else "/tcp"
    print(f"[OPEN] Port {C.BOLD}{port}{suffix:<6}{C.END} {service:<10} [{tag}]")
    print(f"       -> {caption}")


def run_port_scan(target_ip, threads=50):
    all_open = []
    sem = threading.Semaphore(threads)

    print(C.MAGENTA + C.BOLD + f"[*] Starting TCP port scan on {target_ip} ..." + C.END)
    tcp_results = {}
    thread_list = []

    def worker_tcp(p):
        with sem:
            scan_port(target_ip, p, tcp_results, proto="tcp")

    for port in sorted(PORT_INFO.keys()):
        t = threading.Thread(target=worker_tcp, args=(port,))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

    for port in sorted(tcp_results.keys()):
        service, status, caption = PORT_INFO.get(
            port, ("Unknown", "moderate", "Non-standard service, review manually.")
        )
        print_port_line(port, service, status, caption, proto="tcp")
        all_open.append({
            "port": port, "service": service, "status": status,
            "caption": caption, "proto": "tcp"
        })

    if not tcp_results:
        print(C.YELLOW + "  No open TCP ports found among scanned list." + C.END)
    print()

    print(C.MAGENTA + C.BOLD + f"[*] Starting UDP port scan on {target_ip} ..." + C.END)
    udp_results = {}
    thread_list = []

    def worker_udp(p):
        with sem:
            scan_port(target_ip, p, udp_results, proto="udp")

    for port in sorted(UDP_PORT_INFO.keys()):
        t = threading.Thread(target=worker_udp, args=(port,))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

    for port in sorted(udp_results.keys()):
        service, status, caption = UDP_PORT_INFO.get(
            port, ("Unknown", "moderate", "Non-standard UDP service, review manually.")
        )
        print_port_line(port, service, status, caption, proto="udp")
        all_open.append({
            "port": port, "service": service, "status": status,
            "caption": caption, "proto": "udp"
        })

    if not udp_results:
        print(C.YELLOW + "  No open UDP ports found among scanned list." + C.END)
    print()

    return all_open


XSS_PAYLOAD = "<script>alert('wepicrwal_xss_test')</script>"
SQLI_PAYLOADS = ["'", "\" OR \"1\"=\"1", "' OR '1'='1", "1' AND '1'='1"]
SQL_ERROR_SIGNATURES = [
    "you have an error in your sql syntax", "warning: mysql", "unclosed quotation mark",
    "quoted string not properly terminated", "sql syntax", "sqlite3.operationalerror",
    "pg_query()", "postgresql query failed", "ora-01756", "microsoft odbc",
    "odbc sql server driver", "mysql_fetch", "mysqli_fetch",
]

CSRF_TOKEN_HINTS = ["csrf", "token", "authenticity_token", "_token", "nonce"]


def get_forms(url, session):
    try:
        resp = session.get(url, timeout=8, verify=False)
        soup = BeautifulSoup(resp.text, "html.parser")
        return resp, soup.find_all("form")
    except requests.RequestException as e:
        print(C.RED + f"[!] Could not fetch {url}: {e}" + C.END)
        return None, []


def form_details(form, base_url):
    action = form.attrs.get("action", "").strip()
    method = form.attrs.get("method", "get").strip().lower()
    target_url = urljoin(base_url, action) if action else base_url
    inputs = []
    for inp in form.find_all(["input", "textarea", "select"]):
        inputs.append({
            "name": inp.attrs.get("name"),
            "type": inp.attrs.get("type", "text"),
        })
    return {"action": target_url, "method": method, "inputs": inputs}


def submit_form(session, form_info, value):
    data = {}
    for inp in form_info["inputs"]:
        if inp["name"]:
            data[inp["name"]] = value if inp["type"] not in ("submit", "checkbox", "radio") else "on"
    try:
        if form_info["method"] == "post":
            return session.post(form_info["action"], data=data, timeout=8, verify=False)
        else:
            return session.get(form_info["action"], params=data, timeout=8, verify=False)
    except requests.RequestException:
        return None


def check_xss(url, session, forms):
    findings = []
    for form in forms:
        info = form_details(form, url)
        if not info["inputs"]:
            continue
        resp = submit_form(session, info, XSS_PAYLOAD)
        if resp is not None and XSS_PAYLOAD in resp.text:
            findings.append({
                "type": "Reflected XSS",
                "location": f"Form -> {info['action']} [{info['method'].upper()}]",
                "status": "VULNERABLE",
                "caption": "Input is reflected back in the page unescaped. An attacker can inject JavaScript "
                           "to steal cookies/session tokens or deface the page. Fix: HTML-encode all user input "
                           "before rendering, and set a Content-Security-Policy."
            })
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    for param in qs:
        test_qs = qs.copy()
        test_qs[param] = XSS_PAYLOAD
        test_url = urlunparse(parsed._replace(query=urlencode(test_qs, doseq=True)))
        try:
            resp = session.get(test_url, timeout=8, verify=False)
            if XSS_PAYLOAD in resp.text:
                findings.append({
                    "type": "Reflected XSS",
                    "location": f"URL parameter '{param}'",
                    "status": "VULNERABLE",
                    "caption": "Query parameter value is reflected unescaped in the response. "
                               "Fix: HTML-encode output and validate/sanitize input."
                })
        except requests.RequestException:
            pass

    if not findings:
        findings.append({
            "type": "Reflected XSS", "location": "Forms & URL parameters",
            "status": "NOT DETECTED",
            "caption": "No reflected XSS found with basic payload testing. Does not guarantee absence of "
                       "stored/DOM-based XSS - manual review recommended."
        })
    return findings


def check_sqli(url, session, forms):
    findings = []

    def has_sql_error(text):
        low = text.lower()
        return any(sig in low for sig in SQL_ERROR_SIGNATURES)

    for form in forms:
        info = form_details(form, url)
        if not info["inputs"]:
            continue
        vulnerable = False
        for payload in SQLI_PAYLOADS:
            resp = submit_form(session, info, payload)
            if resp is not None and has_sql_error(resp.text):
                vulnerable = True
                break
        findings.append({
            "type": "SQL Injection",
            "location": f"Form -> {info['action']} [{info['method'].upper()}]",
            "status": "VULNERABLE" if vulnerable else "NOT DETECTED",
            "caption": (
                "Database error messages were triggered by SQL meta-characters, indicating unsanitized "
                "input reaching a SQL query. Fix: use parameterized queries / prepared statements."
                if vulnerable else
                "No SQL error signatures triggered with basic payloads. Does not rule out blind/time-based "
                "SQLi - deeper manual testing recommended."
            )
        })

    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    for param in qs:
        vulnerable = False
        for payload in SQLI_PAYLOADS:
            test_qs = qs.copy()
            test_qs[param] = payload
            test_url = urlunparse(parsed._replace(query=urlencode(test_qs, doseq=True)))
            try:
                resp = session.get(test_url, timeout=8, verify=False)
                if has_sql_error(resp.text):
                    vulnerable = True
                    break
            except requests.RequestException:
                pass
        findings.append({
            "type": "SQL Injection",
            "location": f"URL parameter '{param}'",
            "status": "VULNERABLE" if vulnerable else "NOT DETECTED",
            "caption": (
                "Database error triggered via URL parameter - unsanitized input reaching SQL query. "
                "Fix: parameterized queries + input validation."
                if vulnerable else
                "No SQL error signatures triggered. Manual/blind SQLi testing still advised."
            )
        })

    if not findings:
        findings.append({
            "type": "SQL Injection", "location": "N/A",
            "status": "NOT DETECTED",
            "caption": "No forms or URL parameters available to test."
        })
    return findings


def check_csrf(forms, base_url):
    findings = []
    for form in forms:
        info = form_details(form, base_url)
        if info["method"] != "post":
            continue
        names = [(inp["name"] or "").lower() for inp in info["inputs"]]
        has_token = any(any(hint in n for hint in CSRF_TOKEN_HINTS) for n in names)
        findings.append({
            "type": "CSRF",
            "location": f"Form -> {info['action']}",
            "status": "VULNERABLE" if not has_token else "NOT DETECTED",
            "caption": (
                "POST form has no visible CSRF token field. An attacker could trick a logged-in user's "
                "browser into submitting this form. Fix: add a per-session CSRF token validated server-side."
                if not has_token else
                "A token-like field was found in this form. Presence does not guarantee correct server-side "
                "validation - verify manually."
            )
        })
    if not findings:
        findings.append({
            "type": "CSRF", "location": "N/A", "status": "NOT DETECTED",
            "caption": "No POST forms found on the page to evaluate for CSRF protection."
        })
    return findings


def run_vuln_scan(url):
    print(C.MAGENTA + C.BOLD + f"[*] Starting vulnerability scan on {url} ..." + C.END)
    session = requests.Session()
    session.headers.update({"User-Agent": "wepicrwal-scanner/1.0 (authorized-test)"})

    resp, forms = get_forms(url, session)
    if resp is None:
        print(C.RED + "[!] Target unreachable, skipping vulnerability scan." + C.END)
        return []

    print(f"[i] Found {len(forms)} form(s) on the page.")

    all_findings = []
    all_findings += check_xss(url, session, forms)
    all_findings += check_sqli(url, session, forms)
    all_findings += check_csrf(forms, url)

    for f in all_findings:
        if f["status"] == "VULNERABLE":
            tag = C.RED + "VULNERABLE" + C.END
        else:
            tag = C.GREEN + "OK" + C.END
        print(f"[{tag}] {f['type']} @ {f['location']}")
        print(f"     -> {f['caption']}")
    print()
    return all_findings


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>wepicrwal Scan Report - {target}</title>
<style>
  :root {{
    --bg: #0d1117; --panel:#161b22; --border:#30363d; --text:#c9d1d9;
    --safe:#2ea043; --unsafe:#f85149; --moderate:#d29922; --critical:#a40e26;
    --accent:#58a6ff;
  }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', Arial, sans-serif; margin:0; padding:0 0 60px 0; }}
  header {{ background: linear-gradient(90deg,#0d1117,#161b22); border-bottom: 2px solid var(--accent); padding: 30px 40px; text-align:center; }}
  header h1 {{ font-size: 2.4em; margin: 0; letter-spacing: 2px; color: var(--accent); font-family: 'Consolas', monospace; }}
  header p {{ margin: 6px 0 0 0; color:#8b949e; }}
  .credit {{ margin-top:10px; font-size:0.9em; color:#8b949e; }}
  .container {{ max-width: 1000px; margin: 30px auto; padding: 0 20px; }}
  .meta {{ background: var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px 20px; margin-bottom: 30px; }}
  .meta div {{ margin: 4px 0; }}
  h2 {{ border-left: 4px solid var(--accent); padding-left: 10px; margin-top: 40px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; background: var(--panel); border-radius:8px; overflow:hidden;}}
  th, td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; font-size: 0.92em; }}
  th {{ background: #1f2733; color: var(--accent); }}
  tr:hover {{ background: #1c2128; }}
  .badge {{ padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight:bold; color:#0d1117; display:inline-block;}}
  .badge.safe {{ background: var(--safe); }}
  .badge.unsafe, .badge.vuln {{ background: var(--unsafe); color:#fff; }}
  .badge.moderate {{ background: var(--moderate); }}
  .badge.review {{ background: var(--moderate); }}
  .badge.critical {{ background: var(--critical); color:#fff; }}
  .badge.ok {{ background: var(--safe); }}
  .empty {{ color: #8b949e; font-style: italic; padding: 10px 0; }}
  footer {{ text-align:center; margin-top: 60px; color:#8b949e; font-size:0.85em; }}
  .summary-cards {{ display:flex; gap:16px; flex-wrap:wrap; margin-top:12px;}}
  .card {{ background: var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px 22px; flex:1; min-width:140px; text-align:center;}}
  .card .num {{ font-size: 1.8em; font-weight:bold; }}
  .card .label {{ color:#8b949e; font-size:0.85em; margin-top:4px;}}
</style>
</head>
<body>
<header>
  <h1>&lt;/&gt; wepicrwal</h1>
  <p>Web Port &amp; Vulnerability Scan Report</p>
  <div class="credit">Developed by: Md Zishan Raza</div>
</header>
<div class="container">
  <div class="meta">
    <div><b>Target:</b> {target}</div>
    <div><b>Scan Date/Time:</b> {scan_time}</div>
    <div><b>Report Generated By:</b> wepicrwal v1.0</div>
  </div>

  <h2>Summary</h2>
  <div class="summary-cards">
    <div class="card"><div class="num" style="color:var(--accent)">{open_ports_count}</div><div class="label">Open Ports</div></div>
    <div class="card"><div class="num" style="color:var(--unsafe)">{unsafe_ports_count}</div><div class="label">Unsafe / Critical Ports</div></div>
    <div class="card"><div class="num" style="color:var(--unsafe)">{vuln_count}</div><div class="label">Vulnerabilities Found</div></div>
  </div>

  <h2>Port Scan Results</h2>
  {port_table}

  <h2>Vulnerability Scan Results</h2>
  {vuln_table}

  <footer>
    Generated by wepicrwal - for authorized security testing / educational use only.<br>
    Developed by Md Zishan Raza &copy; {year}
  </footer>
</div>
</body>
</html>
"""


def build_port_table(open_ports):
    if not open_ports:
        return '<div class="empty">No open ports were found.</div>'
    rows = ""
    for p in open_ports:
        badge_class = p["status"]
        proto = p.get("proto", "tcp")
        rows += f"""<tr>
            <td>{p['port']}/{proto}</td><td>{html.escape(p['service'])}</td>
            <td><span class="badge {badge_class}">{p['status'].upper()}</span></td>
            <td>{html.escape(p['caption'])}</td>
        </tr>"""
    return f"""<table>
        <tr><th>Port</th><th>Service</th><th>Status</th><th>Risk / Notes</th></tr>
        {rows}
    </table>"""


def build_vuln_table(findings):
    if not findings:
        return '<div class="empty">No vulnerability checks were run.</div>'
    rows = ""
    for f in findings:
        badge_class = "vuln" if f["status"] == "VULNERABLE" else "ok"
        rows += f"""<tr>
            <td>{html.escape(f['type'])}</td>
            <td>{html.escape(f['location'])}</td>
            <td><span class="badge {badge_class}">{f['status']}</span></td>
            <td>{html.escape(f['caption'])}</td>
        </tr>"""
    return f"""<table>
        <tr><th>Vulnerability</th><th>Location</th><th>Status</th><th>Details / Impact</th></tr>
        {rows}
    </table>"""


def safe_filename(name):
    name = re.sub(r"^https?://", "", name)
    name = re.sub(r"[^\w\-.]", "_", name)
    return name.strip("_") or "target"


def generate_html_report(target, open_ports, findings, output_path):
    unsafe_count = sum(1 for p in open_ports if p["status"] in ("unsafe", "critical"))
    vuln_count = sum(1 for f in findings if f["status"] == "VULNERABLE")

    html_out = HTML_TEMPLATE.format(
        target=html.escape(target),
        scan_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        open_ports_count=len(open_ports),
        unsafe_ports_count=unsafe_count,
        vuln_count=vuln_count,
        port_table=build_port_table(open_ports),
        vuln_table=build_vuln_table(findings),
        year=datetime.datetime.now().year,
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(C.GREEN + C.BOLD + f"[+] HTML report saved to: {output_path}" + C.END)


def main():
    parser = argparse.ArgumentParser(
        description="wepicrwal - Web Port & Vulnerability Scanner (authorized use only)"
    )
    parser.add_argument("target", help="Target URL (e.g. http://example.com) or IP/domain")
    parser.add_argument("-o", "--output", default=None,
                        help="HTML report output path (default: auto-unique name)")
    parser.add_argument("--ports-only", action="store_true", help="Run only the port scan")
    parser.add_argument("--vuln-only", action="store_true", help="Run only the vulnerability scan")
    args = parser.parse_args()

    print_banner()

    raw_target = args.target.strip()
    if not raw_target.startswith("http://") and not raw_target.startswith("https://"):
        url = "http://" + raw_target
    else:
        url = raw_target
    parsed = urlparse(url)
    hostname = parsed.hostname

    authorization_gate(hostname)

    try:
        target_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        print(C.RED + f"[!] Could not resolve host: {hostname}" + C.END)
        sys.exit(1)

    print(C.CYAN + f"[i] Resolved {hostname} -> {target_ip}\n" + C.END)

    open_ports = []
    findings = []

    if not args.vuln_only:
        open_ports = run_port_scan(target_ip)

    if not args.ports_only:
        findings = run_vuln_scan(url)

    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_name = safe_filename(hostname)
        output_path = f"wepicrwal_{clean_name}_{timestamp}.html"

    generate_html_report(hostname, open_ports, findings, output_path)

    print(C.BOLD + C.GREEN + "\n[+] Scan complete." + C.END)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(C.RED + "\n[!] Interrupted by user." + C.END)
        sys.exit(1)
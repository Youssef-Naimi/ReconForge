# ReconForge

> Lightweight network reconnaissance toolkit built with Python for learning cybersecurity and network enumeration.

ReconForge is a modular command-line reconnaissance tool that brings together DNS, HTTP, TCP port, banner, and subdomain enumeration in one small project.

The goal is not to replace mature tools such as Nmap. It is a hands-on project for understanding how common reconnaissance techniques work at the Python and network-socket level.

## Features

### DNS reconnaissance

- DNS record enumeration
- A / AAAA records
- MX records
- NS records
- TXT records
- Reverse DNS lookups

### HTTP reconnaissance

- HTTP status code
- Page title
- Redirect detection
- Server and technology-related headers
- Security headers
- Full response headers

### Port reconnaissance

- Common TCP ports
- `OPEN`, `CLOSED`, and `FILTERED` states
- Concurrent scanning with `ThreadPoolExecutor`
- Generic banner grabbing
- HTTP probing
- HTTPS probing with TLS
- Structured scan results

### Subdomain enumeration

- Common subdomain wordlist
- Concurrent DNS resolution
- A / AAAA address discovery
- CNAME detection

## Tech Stack

- **Python 3.14.7**
- **dnspython** — DNS resolution
- **Requests** — HTTP reconnaissance
- **socket** — TCP connections and banner grabbing
- **ssl** — HTTPS/TLS probing
- **concurrent.futures** — concurrent network operations
- **argparse** — command-line interface

## Installation

```bash
git clone https://github.com/Youssef-Naimi/ReconForge.git
cd ReconForge

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

On Windows:

```powershell
.venv\Scripts\activate
```

## Usage

Run ReconForge against a domain you are authorized to assess:

```bash
python -m reconforge.main example.com
```

You can also run the entry point directly:

```bash
python reconforge/main.py example.com
```

ReconForge will perform the currently enabled reconnaissance modules and display the results in the terminal.

## Project Structure

```text
ReconForge/
├── reconforge/
│   ├── __init__.py
│   ├── dns.py
│   ├── http.py
│   ├── ports.py
│   ├── subdomains.py
│   └── main.py
├── requirements.txt
└── README.md
```

### Module responsibilities

| Module | Responsibility |
|---|---|
| `dns.py` | DNS record enumeration and reverse DNS |
| `http.py` | HTTP reconnaissance and header analysis |
| `ports.py` | TCP scanning, banners, HTTP/HTTPS probing |
| `subdomains.py` | Common subdomain discovery and DNS resolution |
| `main.py` | CLI entry point and result presentation |
| `__init__.py` | Python package definition |

## Architecture

```text
                     ReconForge
                          │
                       main.py
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
       DNS               HTTP             Ports
        │                 │                 │
   DNS queries      HTTP requests     TCP connections
                                          │
                              ┌───────────┼───────────┐
                              │           │           │
                           Banners      HTTP        HTTPS
                                          │           │
                                      requests       TLS
        │
   Subdomains
        │
   Concurrent DNS
```

## What I Learned Building It

ReconForge is primarily a learning project. Building it helped me practice:

- Python networking with sockets
- DNS resolution and record handling
- HTTP request/response analysis
- TLS connections
- TCP port states and service banners
- Concurrency for I/O-bound workloads
- Futures and `ThreadPoolExecutor`
- Modular Python project structure
- Exception handling and structured results

## Scope

ReconForge intentionally focuses on **common reconnaissance techniques** rather than trying to become a full replacement for established security tools.

The project currently favors:

- readable Python
- small modules
- reusable functions
- useful raw reconnaissance data
- simple CLI output

## Roadmap

Possible future improvements include:

- Better CLI argument handling
- More protocol-specific probes
- Additional DNS record types
- More robust HTTP/TLS handling
- Automated tests
- Cleaner terminal formatting
- Exporting results to JSON

## Disclaimer

ReconForge is intended for educational purposes and authorized security testing only.

Only scan systems, networks, and domains that you own or have explicit permission to assess.

---

Built as a cybersecurity learning project by **Youssef Naimi**.

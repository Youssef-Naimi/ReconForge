import dns.resolver
from concurrent.futures import ThreadPoolExecutor


COMMON_SUBDOMAINS = [
    "www",
    "mail",
    "ftp",
    "api",
    "app",
    "dev",
    "test",
    "staging",
    "admin",
    "portal",
    "vpn",
    "blog",
    "m",
    "ns1",
    "ns2",
]


def resolve_subdomain(subdomain):
    addresses = []
    cname = None

    for record_type in ("A", "AAAA"):
        try:
            answers = dns.resolver.resolve(subdomain, record_type)

            canonical_name = answers.canonical_name.to_text().rstrip(".")

            if canonical_name != subdomain.rstrip(".") and cname is None:
                cname = canonical_name

            for answer in answers:
                addresses.append(answer.to_text())

        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
            dns.exception.Timeout,
        ):
            continue

    if not addresses:
        return None

    return {
        "addresses": addresses,
        "cname": cname,
    }


def enumerate_subdomains(domain):
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(
                resolve_subdomain,
                f"{prefix}.{domain}"
            ): prefix
            for prefix in COMMON_SUBDOMAINS
        }

        for future in futures:
            prefix = futures[future]

            try:
                result = future.result()
            except Exception:
                continue

            if result:
                results.append({
                    "subdomain": f"{prefix}.{domain}",
                    "addresses": result["addresses"],
                    "cname": result["cname"],
                })

    return results

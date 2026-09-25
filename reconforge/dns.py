import dns.resolver


def get_records(domain):
    record_types = [
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "CNAME"
    ]

    results = {}

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)

            results[record_type] = [
                answer.to_text()
                for answer in answers
            ]
        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers
        ):
            results[record_type] = []

    return results

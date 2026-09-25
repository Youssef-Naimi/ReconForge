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

            if record_type == "MX":
                results[record_type] = [
                    {
                        "priority":  answer.preference,
                        "server":  answer.exchange.to_text()
                    }
                    for answer in answers
                ]
            else:
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

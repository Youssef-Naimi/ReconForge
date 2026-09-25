import dns.resolver
import dns.reversename


def get_records(domain):
    # Different DNS record types to scan for
    record_types = [
        "A",  # IPv4 Record
        "AAAA",  # IPv6 Record
        "MX",  # Mail servers Record
        "NS",  # Name servers associated to this domain
        "TXT",  # Plain text or machine readabble data associated to the domain by it's owner, mainly for verification or email security
        "CNAME"  # Cannonical Name record, used for allowing subdomains, ALWAYS points to a Domain
    ]
    # Results Object
    results = {}
    # looping through records returned to parse them into the results object
    for record_type in record_types:
        try:
            # Collecting Data about the record type
            answers = dns.resolver.resolve(domain, record_type)

            # Special Case: MX (Mail Record) contains special params dictating priority
            if record_type == "MX":
                results[record_type] = [
                    {
                        # Designates the priority assigned to said email server
                        "priority":  answer.preference,
                        # THE EMAIL SERVER, PS: parsing to text since it's an object data type
                        "server":  answer.exchange.to_text()
                    }
                    for answer in answers
                ]
            else:
                results[record_type] = [
                    answer.to_text()  # Again, parsing to text since object data type
                    for answer in answers
                ]
        except (
            dns.resolver.NoAnswer,  # server doesn't reply
            dns.resolver.NXDOMAIN,  # Non Existant Domain
            # No DNS Server answers said query, could be DNS down as well as bad response
            dns.resolver.NoNameservers
        ):
            # said record type goes empty when one of these exceptions occur
            results[record_type] = []

    return results


def reverse_lookup(ip_addr):
    try:
        # Gets domain name associated to the address given to said IP, mainly for fetching hostnames
        reverse_name = dns.reversename.from_address(ip_addr)

        answers = dns.resolver.resolve(
            reverse_name,  # domain name
            "PTR"  # Record that contains the domain name of an IP address
        )

        return [
            answer.to_text()  # once again, to text since answer is an object data type
            for answer in answers
        ]
    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
        dns.exception.Timeout  # server answer timedout
    ):
        return []

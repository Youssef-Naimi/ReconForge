import argparse
from reconforge.dns import get_records, reverse_lookup


def main():
    parser = argparse.ArgumentParser(
        description="ReconForge - Security Reconnaissance Framework"
    )

    parser.add_argument(
        "target",
        help="Target domain or IP address"
    )

    args = parser.parse_args()

    print(f"[+] Target: {args.target}")
    print(f"\n[+] DNS: ")

    records = get_records(args.target)

    for record_type, values in records.items():
        print(f"\n{record_type}:")

        if not values:
            print(f"    None")
            continue
        for value in values:
            if record_type == "MX":
                print(
                    f"  {value['priority']}"
                    f"  {value['server']}"
                )
            else:
                print(f"    {value}")

    print("\n[+] REVERSE DNS:")

    for ip_address in records["A"]:
        hostnames = reverse_lookup(ip_address)

        print(f"\n{ip_address}:")

        if hostnames:
            for hostname in hostnames:
                print(f"    {hostname}")
        else:
            print("    None")


if __name__ == "__main__":
    main()

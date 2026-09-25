import argparse
from reconforge.dns import get_records


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

        if values:
            for value in values:
                print(f"    {value}")
        else:
            print(f"    None")


if __name__ == "__main__":
    main()

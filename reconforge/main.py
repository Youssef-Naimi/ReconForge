import argparse
from reconforge.dns import get_records, reverse_lookup
from reconforge.http import get_http_info


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
        print(f"\n    {record_type}:")

        if not values:
            print(f"        None")
            continue
        for value in values:
            if record_type == "MX":
                print(
                    f"        {value['priority']}"
                    f"        {value['server']}"
                )
            else:
                print(f"        {value}")

    print("\n[+] REVERSE DNS:")

    for ip_address in records["A"]:
        hostnames = reverse_lookup(ip_address)

        print(f"\n    {ip_address}:")

        if hostnames:
            for hostname in hostnames:
                print(f"        {hostname}")
        else:
            print("        None")

    print("\n[+] HTTP:")

    http_info = get_http_info(f"http://{args.target}")

    if http_info:
        print(f"    Url:    {http_info["url"]}")
        print(f"    Status:    {http_info["status_code"]}")
        print(f"    Title:    {http_info["title"]}")
        print("    Server Information:")

        if http_info["server"]:
            for header, value in http_info["server"].items():
                print(f"        {header}: {value}")
        else:
            print("        None")

        print("\n    Security Headers:")

        for header, value in http_info["security_headers"].items():
            if value:
                print(f"        {header}: PRESENT")
            else:
                print(f"        {header}: MISSING")

        print("\n    Redirects:")

        if http_info["redirects"]:
            for redirect in http_info["redirects"]:
                print(
                    f"        {redirect['status_code']} "
                    f"{redirect['url']} -> "
                    f"{redirect['location']}"
                )
        else:
            print("        None")

        print("\n    Headers:")

        for name, value in http_info["headers"].items():
            print(f"        {name}: {value}")
    else:
        print("Unable to connect")


if __name__ == "__main__":
    main()

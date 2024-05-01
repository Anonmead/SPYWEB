import argparse
import socket
from colorama import Fore
import requests
import whois

text = """
██╗███╗   ██╗███████╗ ██████╗ 
██║████╗  ██║██╔════╝██╔═══██╗
██║██╔██╗ ██║█████╗  ██║   ██║
██║██║╚██╗██║██╔══╝  ██║   ██║
██║██║ ╚████║██║     ╚██████╔╝
╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
"""
print(f"{Fore.CYAN}{text}{Fore.WHITE}")
print(f"{Fore.BLUE}Creator: d0ct0r{Fore.WHITE}")
print()
print()


def scan_domain(domain: str):
    s = requests.Session()
    try:
        r = s.get(domain, verify=True, timeout=5)
    except requests.exceptions.MissingSchema:
        print(f"{Fore.RED}[-]{Fore.WHITE}Please provide a valid URL with schema (e.g., https://example.com)")
        return

    servers = []
    for v, k in r.headers.items():
        if "Server" in v:
            servers.append(k)
        else:
            pass

    if "https://" in domain:
        domain = domain.replace("https://", "")
    if "https://" in domain:
        domain = domain.replace("https://www.", "")

    ip = socket.gethostbyname(domain)

    try:
        with open("get_info.txt", "a") as f:
            if r.status_code == 200:
                f.write("[+] Server Information\n")
                f.write(f"Domain: {domain}\n")
                f.write(f"IP Address: {ip}\n")
                f.write(f"Servers: {', '.join(map(str, servers))}\n\n")
                print(f"{Fore.GREEN}[+] {Fore.WHITE}- {domain} ({ip})({', '.join(map(str, servers))})")
            else:
                f.write("[-] Website Not Reachable\n")
                f.write(f"Domain: {domain}\n\n")
                print(f"{Fore.RED}[-] {Fore.WHITE} - {domain}")
    except FileNotFoundError:
        print("File Not Found")

def get_whois_info(domain):
    try:
        whois_info = whois.whois(domain)
        return whois_info
    except whois.parser.PywhoisError as e:
        print("Error:", e)
        return None

def main():
    parser = argparse.ArgumentParser(description="Scan website and retrieve WHOIS information")
    parser.add_argument("-t", "--targets", help="Target URL to scan", required=True)
    parser.add_argument("--info", "--information", help="Retrieve WHOIS information", action="store_true")
    parser.add_argument("--save", help="Save results to a file with specified filename")
    args = parser.parse_args()

    scan_website = args.targets
    scan_domain(scan_website)

    if args.info:
        whois_info = get_whois_info(scan_website)
        if whois_info:
            print("WHOIS information for", scan_website)
            print(whois_info)

    if args.save:
        filename = args.save
        try:
            with open(filename, "a") as f:
                f.write(f"[+] Results for {scan_website}:\n")
                f.write("-------------\n")
                if args.info and whois_info:
                    f.write("WHOIS information:\n")
                    f.write(str(whois_info))
                    f.write("\n")
                f.write("\n")
                print(f"{Fore.GREEN}[+]{Fore.WHITE}Results saved to {filename}")
        except FileNotFoundError:
            print(f"{Fore.RED}[-]{Fore.WHITE}Error: File {filename} not found.")

if __name__ == "__main__":
    main()

from colorama import Fore
import dns.resolver
import argparse
import sys

text = """
██████╗ ███╗   ██╗███████╗              ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗████╗  ██║██╔════╝              ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██║  ██║██╔██╗ ██║███████╗    █████╗    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██║  ██║██║╚██╗██║╚════██║    ╚════╝    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██████╔╝██║ ╚████║███████║              ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
"""
print(f"{Fore.YELLOW}{text}{Fore.WHITE}")
print(f"{Fore.BLUE}Creator: d0ct0r{Fore.WHITE}")
print()
print()

def perform_dns_recon(domains, output_file=None):
    record_types = ['A', 'AAAA', 'NS', 'CNAME', 'MX', 'PTR', 'SOA', 'TXT']

    try:
        if output_file is not None:
            with open(output_file, "w") as f:
                for domain in domains:
                    output_text = f"DNS Reconnaissance for: {domain}\n"
                    f.write(output_text)
                    for record in record_types:
                        try:
                            answer = dns.resolver.resolve(domain, record)
                            output_text = f"\n{record} Records\n" + "-" * 30 + "\n"
                            for server in answer:
                                record_info = server.to_text()
                                output_text += record_info + "\n"
                            print(output_text)  # Print to console
                            f.write(output_text)  # Write to file
                        except dns.resolver.NoAnswer:
                            pass
                        except dns.resolver.NXDOMAIN:
                            output_text = f"{Fore.RED}[-] {Fore.WHITE} {domain} does not exist.\n"
                            print(output_text)  # Print to console
                            f.write(output_text)  # Write to file
                            break
                        except KeyboardInterrupt:
                            output_text = f"{Fore.RED}[-] {Fore.WHITE}DNS reconnaissance interrupted by user.\n"
                            print(output_text)  # Print to console
                            f.write(output_text)  # Write to file
                            return
        else:
            for domain in domains:
                output_text = f"DNS Reconnaissance for: {domain}\n"
                print(output_text)
                for record in record_types:
                    try:
                        answer = dns.resolver.resolve(domain, record)
                        output_text = f"\n{record} Records\n" + "-" * 30 + "\n"
                        for server in answer:
                            record_info = server.to_text()
                            output_text += record_info + "\n"
                        print(output_text)  # Print to console
                    except dns.resolver.NoAnswer:
                        pass
                    except dns.resolver.NXDOMAIN:
                        output_text = f"{Fore.RED}[-] {Fore.WHITE} {domain} does not exist.\n"
                        print(output_text)  # Print to console
                        break
                    except KeyboardInterrupt:
                        output_text = f"{Fore.RED}[-] {Fore.WHITE}DNS reconnaissance interrupted by user.\n"
                        print(output_text)  # Print to console
                        return
    except IOError:
        print(f"{Fore.RED}[-] {Fore.WHITE}Error: Failed to write to file {output_file}")
        return

    if output_file:
        print(f"{Fore.GREEN}[+] {Fore.WHITE}DNS reconnaissance information saved to {output_file}")

# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform DNS reconnaissance on domain(s)")
    parser.add_argument("-t", "--targets", help="Domain name(s) to perform DNS reconnaissance on", nargs="+", required=True)
    parser.add_argument("--dns", help="Perform DNS reconnaissance on the specified domain(s)", action="store_true")
    parser.add_argument("--save", help="Save the DNS reconnaissance information to a file", action="store_true")
    args = parser.parse_args()

    domains = args.targets

    if args.dns:
        perform_dns_recon(domains, "dns_recon_output.txt" if args.save else None)
    else:
        print(f"{Fore.RED}[-] {Fore.WHITE}Please specify the --dns option to perform DNS reconnaissance.")

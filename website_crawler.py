import requests
from bs4 import BeautifulSoup
import socket
from colorama import Fore, Style
from urllib.parse import urljoin, urlparse
import re
import fade
import argparse

text = """
██╗    ██╗███████╗██████╗ ███████╗██╗████████╗███████╗         ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ 
██║    ██║██╔════╝██╔══██╗██╔════╝██║╚══██╔══╝██╔════╝        ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
██║ █╗ ██║█████╗  ██████╔╝███████╗██║   ██║   █████╗          ██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
██║███╗██║██╔══╝  ██╔══██╗╚════██║██║   ██║   ██╔══╝          ██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
╚███╔███╔╝███████╗██████╔╝███████║██║   ██║   ███████╗███████╗╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
"""
print(fade.random(text))
print(f"{Fore.BLUE}Creator: d0ct0r{Fore.WHITE}")
print()
print()

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def get_robots_txt(url):
    domain = get_domain(url)
    robots_url = urljoin(domain, "robots.txt")
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.WHITE}Error retrieving robots.txt: {e}")
        return None

def parse_robots_txt(robots_txt):
    disallowed = []
    allowed = []
    lines = robots_txt.split('\n')
    user_agent = None
    for line in lines:
        if line.startswith('User-agent:'):
            user_agent_split = line.split(': ')
            if len(user_agent_split) > 1:
                user_agent = user_agent_split[1]
        elif line.startswith('Disallow:') and user_agent == '*' and len(line.split(': ')) > 1 and len(line.split(': ')[1]) > 0:
            disallowed.append(line.split(': ')[1])
        elif line.startswith('Allow:') and user_agent == '*' and len(line.split(': ')) > 1 and len(line.split(': ')[1]) > 0:
            allowed.append(line.split(': ')[1])
        else:
            print(f"Skipping line: {line}")  # Debugging statement
    return disallowed, allowed

def is_allowed(url, disallowed, allowed):
    url_path = urlparse(url).path
    for disallow in disallowed:
        if re.match(disallow, url_path):
            return False
    for allow in allowed:
        if re.match(allow, url_path):
            return True
    return True

def find_links(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        found_links = []
        for link in links:
            href = link['href']
            absolute_url = urljoin(url, href)
            found_links.append(absolute_url)
        return found_links
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.WHITE}Error finding links for {url}: {e}")
        return []

def get_ip_address(url):
    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"Error getting IP for {url}: {e}")
        return None

def crawl(url, depth=2):
    try:
        visited = set()
        results = []
        robots_txt = get_robots_txt(url)
        if robots_txt:
            disallowed, allowed = parse_robots_txt(robots_txt)
        else:
            disallowed, allowed = [], []
        crawl_recursive(url, depth, visited, disallowed, allowed, results)
        return results
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.WHITE}Error scanning website: {e}")
        return []

def crawl_recursive(url, depth, visited, disallowed, allowed, results):
    if depth <= 0 or url in visited:
        return
    visited.add(url)
    ip = get_ip_address(url)
    print(f"{Fore.GREEN}[+] {Fore.WHITE}Crawling: {Style.BRIGHT}{url}{Style.RESET_ALL}", end='')
    if ip:
        print(f" {Fore.GREEN}(IP: {Style.BRIGHT}{ip}{Style.RESET_ALL})")
        results.append(f"{url}: {Fore.GREEN}{ip}{Fore.WHITE}\n")
    else:
        print(f"{Fore.RED} [Failed to get IP]{Fore.WHITE}")
        results.append(f"{url}: {Fore.RED}Failed to get IP{Fore.WHITE}\n")
    links = find_links(url)
    for link in links:
        if is_allowed(link, disallowed, allowed):
            crawl_recursive(link, depth - 1, visited, disallowed, allowed, results)
        else:
            print(f"{Fore.YELLOW}[!] {Fore.WHITE}Skipping disallowed link: {link}")


    if any(link.endswith(".php") for link in links):
        print(f"{Fore.RED}[Vulnerability Found] PHP file detected on {url}")
        results.append(f"{url}: {Fore.RED}PHP file detected{Fore.WHITE}\n")


    if any(".php?id" in link for link in links):
        print(f"{Fore.YELLOW}[Potential Vulnerability]{Fore.WHITE} {url}")
        results.append(f"{url}: {Fore.YELLOW}Page with .php?id detected{Fore.WHITE}\n")


    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            if "SQL error" in response.text or "SQL syntax" in response.text:
                print(f"{Fore.RED}[Vulnerability Found] SQL injection detected on {url}")
                results.append(f"{url}: {Fore.RED}SQL injection detected{Fore.WHITE}\n")
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.WHITE}Error checking for SQL injection on {url}: {e}")

def save_results_to_file(results, filename):
    with open(filename, 'w') as file:
        for result in results:
            file.write(result)
    print(f"{Fore.GREEN}[+] {Fore.WHITE}Results saved to {Style.BRIGHT}{filename}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Website Crawler")
    parser.add_argument("-t", "--targets", nargs="+", help="Target URLs", required=True)
    parser.add_argument("--depth", type=int, default=2, help="Depth of crawling (default is 2)")
    parser.add_argument("--save", type=str, help="Save results to a file with the specified filename")
    args = parser.parse_args()

    all_results = []

    for target_url in args.targets:
        print(f"{Fore.RED}{Style.BRIGHT}[+] {Fore.WHITE}Initializing {Style.BRIGHT}Scanning{Style.RESET_ALL} for {Style.BRIGHT}{target_url}{Style.RESET_ALL}...\n")
        results = crawl(target_url, args.depth)
        all_results.extend(results)

    print(f"\n{Fore.RED}{Style.BRIGHT}[+] {Fore.WHITE}{Style.BRIGHT}Scanning{Style.RESET_ALL} complete. {Fore.RED}{Style.BRIGHT}Exiting...{Style.RESET_ALL}\n")

    if args.save:
        save_results_to_file(all_results, args.save)

if __name__ == "__main__":
    main()
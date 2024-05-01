import argparse
from colorama import Fore
import validators
import requests
from urllib.parse import urlparse
import socket

text = """
 ██████╗██████╗  █████╗ ██╗    ██╗██╗      ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗      ██╗     ██╗███████╗████████╗
██╔════╝██╔══██╗██╔══██╗██║    ██║██║      ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║      ██║     ██║██╔════╝╚══██╔══╝
██║     ██████╔╝███████║██║ █╗ ██║██║█████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║█████╗██║     ██║███████╗   ██║   
██║     ██╔══██╗██╔══██║██║███╗██║██║╚════╝██║███╗██║██║   ██║██╔══██╗██║  ██║██║╚════╝██║     ██║╚════██║   ██║   
╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗ ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗ ███████╗██║███████║   ██║  
"""
print(f"{Fore.GREEN}{text}{Fore.WHITE}")
print(f"{Fore.BLUE}Creator: d0ct0r{Fore.WHITE}")
print()
print()


def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def save_links_to_file(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')
    print(f"{Fore.GREEN}[+]{Fore.WHITE} File Saved In {filename}{Fore.WHITE}")

def get_wordlist_from_file(wordlist_filename):
    try:
        with open(wordlist_filename, 'r') as wordlist_file:
            wordlist = wordlist_file.readlines()
            return [word.strip() for word in wordlist]
    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Fore.WHITE} Wordlist file not found.")
        return None

def crawl(domain, wordlist_filename, save_links):
    try:
        if not validators.url(domain):
            print(f"{Fore.RED}[-]{Fore.WHITE} Invalid URL format. Please provide a valid URL (e.g., https://example.com)")
            return

        wordlist = get_wordlist_from_file(wordlist_filename)
        if not wordlist:
            return

        valid_links = []

        for word in wordlist:
            url_with_word = f"{domain}/{word}"
            response = requests.get(url_with_word)

            if response.status_code in [200, 403]:
                ip_address = get_ip_address(urlparse(domain).netloc)
                print(f"{Fore.GREEN}[+]{Fore.WHITE} URL: {url_with_word} | IP: {Fore.LIGHTRED_EX}{ip_address or 'N/A'}{Fore.WHITE} | {Fore.GREEN}Page Found{Fore.WHITE}")
                valid_links.append(url_with_word)
            elif response.status_code == 404:
                print(f"{Fore.RED}[-]{Fore.WHITE} URL: {url_with_word} | {Fore.RED}Page Not Found{Fore.WHITE}")
            elif response.status_code == 400:
                print(f"{Fore.RED}[-]{Fore.WHITE} URL: {url_with_word} | {Fore.RED}Bad Request{Fore.WHITE}")
            else:
                print(f"{Fore.RED}[-]{Fore.WHITE} URL: {url_with_word} | {Fore.RED}Unknown Error{Fore.WHITE}")

        if save_links:
            save_links_to_file(valid_links, "website_crawler_wordlist_save_link.txt")
        else:
            print(f"{Fore.RED}[-]{Fore.WHITE} Links not saved.")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] {Fore.WHITE}Failed to connect: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Crawler with Wordlist")
    parser.add_argument("-t", "--target", help="Target domain URL", required=True)
    parser.add_argument("--wl", "--wordlist", help="Wordlist filename", required=True, dest="wordlist_filename")
    parser.add_argument("--save", help="Save links to a file with the specified filename")
    args = parser.parse_args()

    crawl(args.target, args.wordlist_filename, args.save)

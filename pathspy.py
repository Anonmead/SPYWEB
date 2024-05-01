from colorama import Fore
import validators
import requests
import argparse


banner = """
██████   █████  ████████ ██   ██ ███████ ██████  ██    ██ 
██   ██ ██   ██    ██    ██   ██ ██      ██   ██  ██  ██  
██████  ███████    ██    ███████ ███████ ██████    ████   
██      ██   ██    ██    ██   ██      ██ ██         ██    
██      ██   ██    ██    ██   ██ ███████ ██         ██ 
"""

def save_links_to_file(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')
        print(f"{Fore.GREEN}[+]{Fore.WHITE} File Saved In {filename}{Fore.WHITE}")

def check_website(target_url, wordlist_filename, save_filename=None):
    try:
        if not validators.url(target_url):
            print(f"{Fore.RED}[-]{Fore.WHITE} Invalid URL: <https://example.com>")
            return

        try:
            with open('pathspy', 'r') as wordlist_file:
                wordlist = wordlist_file.readlines()
        except FileNotFoundError:
            print(f"{Fore.RED}[-]{Fore.WHITE} Wordlist file not found.")
            return

        wordlist = [word.strip() for word in wordlist]
        valid_links = []

        for word in wordlist:
            url_with_word = f"{target_url}/{word}"

            response = requests.get(url_with_word)

            if response.status_code == 200:
                print(f"{Fore.GREEN}[+]{Fore.WHITE} URL: {url_with_word} | {Fore.GREEN}Page Found{Fore.WHITE} | ")
                valid_links.append(url_with_word)
            elif response.status_code == 403:
                print(f"{Fore.YELLOW}[?]{Fore.WHITE} URL: {url_with_word}  |{Fore.YELLOW}You do not have access to this page{Fore.WHITE}")
            else:
                print(f"{Fore.RED}[-]{Fore.WHITE} URL: {url_with_word} | {Fore.RED}Error: {response.status_code}{Fore.WHITE}")

        if save_filename:
            save_links_to_file(valid_links, save_filename)
        else:
            print(f"{Fore.RED}[-]{Fore.WHITE} Links not saved.")
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[-] {Fore.WHITE}Failed to connect")

def main():
    print(f"{Fore.CYAN}{banner}{Fore.WHITE}")
    parser = argparse.ArgumentParser(description="Check Website for Valid Links")
    parser.add_argument("-t", "--targets", help="Target URL", required=True)
    parser.add_argument("--wl", "--wordlist", help="Wordlist filename", required=True)
    parser.add_argument("--save", help="Save links to a file with the specified filename")
    args = parser.parse_args()

    check_website(args.targets, args.wl, args.save)  # Change args.wordlist to args.wl

if __name__ == "__main__":
    main()


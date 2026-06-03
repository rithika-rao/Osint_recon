import requests
import json
from colorama import Fore, Style

WMN_URL = "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"

TOP_SITES = [
    "GitHub (User)", "Reddit", "Instagram", "TikTok",
    "YouTube Channel", "Pinterest", "Twitch", "Steam",
    "Spotify", "Snapchat", "Flickr", "Vimeo", "Tumblr",
    "DeviantArt", "Pastebin", "HackerNews", "Keybase", "GitLab",
    "Mastodon", "Roblox"
]

def load_wmn_data():
    print(f"{Fore.CYAN}[*] Fetching WhatsMyName dataset...{Style.RESET_ALL}")
    try:
        r = requests.get(WMN_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        sites = data.get("sites", [])
        filtered = [s for s in sites if s.get("name") in TOP_SITES]
        print(f"{Fore.CYAN}[*] Loaded {len(filtered)} sites to check{Style.RESET_ALL}")
        return filtered
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to load WMN data: {e}{Style.RESET_ALL}")
        return []

def check_username(username):
    print(f"\n{Fore.YELLOW}[~] Searching username: {username}{Style.RESET_ALL}\n")
    sites = load_wmn_data()
    found = []
    not_found = []
    errors = []

    headers = {"User-Agent": "osint-recon/1.0"}

    for site in sites:
        name = site.get("name", "unknown")
        uri = site.get("uri_check", "").replace("{account}", username)
        account_existence_code = site.get("account_existence_code", 200)

        if not uri:
            continue

        try:
            r = requests.get(uri, headers=headers, timeout=8, allow_redirects=True)
            if r.status_code == account_existence_code:
                print(f"  {Fore.GREEN}[+] FOUND    {name:<20} {uri}{Style.RESET_ALL}")
                found.append({"site": name, "url": uri})
            else:
                print(f"  {Fore.RED}[-] not found {name}{Style.RESET_ALL}")
                not_found.append(name)
        except requests.exceptions.Timeout:
            print(f"  {Fore.YELLOW}[?] timeout   {name}{Style.RESET_ALL}")
            errors.append(name)
        except Exception:
            errors.append(name)

    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Found:     {len(found)}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Not found: {len(not_found)}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Errors:    {len(errors)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

    return found

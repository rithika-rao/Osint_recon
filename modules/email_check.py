import requests
import hashlib
from colorama import Fore, Style

def check_email_breaches(email):
    print(f"\n{Fore.YELLOW}[~] Checking email for breaches: {email}{Style.RESET_ALL}\n")

    url = f"https://breachdirectory.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "PASTE_YOUR_RAPIDAPI_KEY_HERE",
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
    }
    params = {"func": "auto", "term": email}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("success") and data.get("result"):
                results = data["result"]
                print(f"  {Fore.RED}[!] Email found in {len(results)} breach(es)!{Style.RESET_ALL}\n")
                for breach in results[:5]:
                    sources = breach.get("sources", ["Unknown"])
                    password_hint = breach.get("password", "hidden")
                    print(f"  {Fore.RED}  -> Sources: {', '.join(sources)}{Style.RESET_ALL}")
                    print(f"       Password hint: {password_hint}\n")
                return results
            else:
                print(f"  {Fore.GREEN}[+] No breaches found for this email.{Style.RESET_ALL}")
                return []
        elif r.status_code == 401:
            print(f"  {Fore.YELLOW}[!] No API key set — skipping breach check.{Style.RESET_ALL}")
            print(f"      Get a free key at: https://rapidapi.com/rohan-patra/api/breachdirectory{Style.RESET_ALL}")
            return []
        else:
            print(f"  {Fore.RED}[!] API error: {r.status_code}{Style.RESET_ALL}")
            return []
    except Exception as e:
        print(f"  {Fore.RED}[!] Request failed: {e}{Style.RESET_ALL}")
        return []


def check_password_pwned(password):
    print(f"\n{Fore.YELLOW}[~] Checking password against HIBP Pwned Passwords...{Style.RESET_ALL}\n")

    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    try:
        r = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={
                "User-Agent": "osint-recon/1.0",
                "Add-Padding": "true"
            },
            timeout=8
        )
        r.raise_for_status()

        hashes = (line.split(":") for line in r.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                count = int(count)
                print(f"  {Fore.RED}[!] Password has been seen {count:,} times in data breaches!{Style.RESET_ALL}")
                print(f"      Do NOT use this password.\n")
                return count

        print(f"  {Fore.GREEN}[+] Password not found in any known breach. Good!{Style.RESET_ALL}\n")
        return 0

    except Exception as e:
        print(f"  {Fore.RED}[!] HIBP request failed: {e}{Style.RESET_ALL}")
        return -1

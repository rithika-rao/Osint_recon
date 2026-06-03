import argparse
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

from modules.username import check_username
from modules.email_check import check_email_breaches, check_password_pwned

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
  ____  ____  ___ _   _ _____      ____  _____ ____ ___  _   _ 
 / __ \/ ___||_ _| \ | |_   _|    |  _ \| ____/ ___/ _ \| \ | |
| |  | \___ \ | ||  \| | | |______| |_) |  _|| |  | | | |  \| |
| |__| |___) || || |\  | | |______|  _ <| |__| |__| |_| | |\  |
 \____/|____/___|_| \_| |_|      |_| \_\_____\____\___/|_| \_|
{Style.RESET_ALL}
{Fore.YELLOW}  OSINT Recon Tool — Username & Email Investigator
  Built using the Awesome-OSINT-List dataset
{Style.RESET_ALL}"""

def save_report(data, filename):
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n{Fore.CYAN}[*] Report saved to: {path}{Style.RESET_ALL}")

def run_username_mode(username, save):
    found = check_username(username)
    if save:
        report = {
            "type": "username",
            "target": username,
            "timestamp": datetime.now().isoformat(),
            "found_on": found
        }
        save_report(report, f"username_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def run_email_mode(email, save):
    breaches = check_email_breaches(email)
    if save:
        report = {
            "type": "email",
            "target": email,
            "timestamp": datetime.now().isoformat(),
            "breaches": breaches
        }
        save_report(report, f"email_{email.replace('@','_at_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def run_password_mode(password):
    check_password_pwned(password)
    print(f"{Fore.YELLOW}  [!] Password not saved to disk or any report.{Style.RESET_ALL}")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="osint-recon: CLI username & email investigator",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--username", "-u",
        metavar="USERNAME",
        help="Search a username across 20+ platforms"
    )
    parser.add_argument(
        "--email", "-e",
        metavar="EMAIL",
        help="Check an email address for data breaches"
    )
    parser.add_argument(
        "--password", "-p",
        metavar="PASSWORD",
        help="Check if a password has appeared in known breaches (HIBP)"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Save results to a JSON report in /reports"
    )
    parser.add_argument(
        "--all", "-a",
        metavar="TARGET",
        help="Run username + email checks on a single target"
    )

    args = parser.parse_args()

    if not any([args.username, args.email, args.password, args.all]):
        parser.print_help()
        return

    if args.all:
        run_username_mode(args.all, args.save)
        run_email_mode(args.all, args.save)

    if args.username:
        run_username_mode(args.username, args.save)

    if args.email:
        run_email_mode(args.email, args.save)

    if args.password:
        run_password_mode(args.password)

if __name__ == "__main__":
    main()

# osint-recon

A beginner-friendly OSINT CLI tool for username enumeration and email breach checking, built using tools from the [Awesome-OSINT-List](https://github.com/Astrosp/Awesome-OSINT-List).

## Features

- **Username search** — checks a username across 20+ platforms (GitHub, Reddit, Instagram, TikTok, Steam, etc.) using the [WhatsMyName](https://github.com/WebBreacher/WhatsMyName) dataset
- **Email breach check** — queries BreachDirectory to see if an email appeared in known data leaks
- **Password check** — uses the HIBP k-anonymity API to check if a password has been exposed (your password is never sent in full)
- **JSON reports** — save results to a timestamped file with `--save`

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/osint-recon.git
cd osint-recon
pip install -r requirements.txt
```

## Usage

```bash
# Search a username across platforms
python osint_recon.py --username hacker123

# Check an email for breaches
python osint_recon.py --email target@example.com

# Check a password against HIBP (100% free, no key needed)
python osint_recon.py --password mysecretpassword

# Run username + email together and save a report
python osint_recon.py --all hacker123 --save
```

## Setup (Email Breach Check)

The email breach check uses the BreachDirectory API via RapidAPI.

1. Sign up free at [rapidapi.com](https://rapidapi.com/rohan-patra/api/breachdirectory)
2. Copy your API key
3. Open `modules/email_check.py` and replace `PASTE_YOUR_RAPIDAPI_KEY_HERE` with your key

> The password check (`--password`) uses HIBP's Pwned Passwords API which is **completely free** — no key needed.

## How it works

### Username search
Downloads the WhatsMyName JSON dataset from GitHub, filters it to the top 20 platforms, then sends a real HTTP request to each site's profile URL. If the response code matches what a real profile returns, the account is marked as found.

### Password check
Uses k-anonymity: only the first 5 characters of the SHA-1 hash of your password are sent to HIBP. They return all hashes starting with those 5 characters, and the comparison is done locally. Your actual password never leaves your machine.

## Legal & ethical use

This tool is for **educational and authorised research purposes only**. Only investigate accounts and emails you own or have explicit permission to test. Unauthorised OSINT on individuals may be illegal depending on your jurisdiction.

## Data sources

- [WhatsMyName](https://github.com/WebBreacher/WhatsMyName) — username enumeration dataset
- [BreachDirectory](https://breachdirectory.org/) — breach data
- [HaveIBeenPwned](https://haveibeenpwned.com/) — Pwned Passwords API

## Roadmap

- [ ] Add Sherlock integration
- [ ] Add Shodan IP lookup module
- [ ] Export results as HTML report
- [ ] Add `--verbose` flag for full HTTP response details

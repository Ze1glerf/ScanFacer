#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScanFacer - Interactive Website Scanner with Optional Zero Delay
Author: Ze1glerf
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import time


def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

clear_console()


ASCII_ART = r"""
 $$$$$$\                               $$$$$$$$\                                     
$$  __$$\                              $$  _____|                                    
$$ /  \__| $$$$$$$\ $$$$$$\  $$$$$$$\  $$ |   $$$$$$\   $$$$$$$\  $$$$$$\   $$$$$$\  
\$$$$$$\  $$  _____|\____$$\ $$  __$$\ $$$$$\ \____$$\ $$  _____|$$  __$$\ $$  __$$\ 
 \____$$\ $$ /      $$$$$$$ |$$ |  $$ |$$  __|$$$$$$$ |$$ /      $$$$$$$$ |$$ |  \__|
$$\   $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$  __$$ |$$ |      $$   ____|$$ |      
\$$$$$$  |\$$$$$$$\\$$$$$$$ |$$ |  $$ |$$ |  \$$$$$$$ |\$$$$$$$\ \$$$$$$$\ $$ |      
 \______/  \_______|\_______|\__|  \__|\__|   \_______| \_______| \_______|\__|      

Made by Ze1glerf | GitHub : Ze1glerf
"""

GREEN = "\033[32m"
RESET = "\033[0m"

print(GREEN + ASCII_ART + RESET)

visited_urls = set()
discovered_links = []

def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def get_domain(url: str) -> str:
    return urlparse(url).netloc.replace("www.", "")

def crawl(url: str, delay_seconds: float, depth: int = 3, base_domain: str = ""):
    if url in visited_urls or depth == 0:
        return

    print(f"[+] Crawling: {url} (depth={depth})")
    visited_urls.add(url)
    discovered_links.append(url)

    try:
        response = requests.get(url, timeout=10)
        
        
        if delay_seconds > 0:
            time.sleep(delay_seconds)

        if "text/html" not in response.headers.get("Content-Type", ""):
            return

        soup = BeautifulSoup(response.text, "html.parser")
        for anchor in soup.find_all("a", href=True):
            href = anchor.get("href")
            next_url = urljoin(url, href)
            if is_valid_url(next_url):
                parsed_next = urlparse(next_url)
                if parsed_next.netloc.endswith(base_domain):
                    crawl(next_url, delay_seconds, depth - 1, base_domain)

    except requests.RequestException as e:
        print(f"[!] Request failed: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

def save_to_file(base_url: str):
    domain = get_domain(base_url)
    time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{domain}_{time_str}.txt"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(f"Website: {base_url}\n")
            file.write(f"Scan Time: {datetime.now()}\n")
            file.write(f"Discovered Pages ({len(discovered_links)} total):\n")
            file.write("-" * 60 + "\n")
            for link in sorted(discovered_links):
                file.write(f"{link}\n")
        print(f"\n✅ Scan complete. Results saved to: {filename}")

    except IOError as io_err:
        print(f"[!] Failed to write file: {io_err}")

def main():
    domain = input("🌐 Enter domain (e.g. example.com): ").strip()

    protocol_choice = input("🔐 Use HTTPS? (yes/no) [yes]: ").strip().lower()
    if protocol_choice in ["no", "n"]:
        protocol = "http"
    else:
        protocol = "https"

    delay_input = input("⏱️ Delay between requests in seconds? (0 for no delay, recommended 20): ").strip()
    try:
        delay_seconds = float(delay_input) if delay_input else 20.0
        if delay_seconds < 0:
            print("⚠️ Negative delay not allowed. Using default 20 seconds.")
            delay_seconds = 20.0
    except ValueError:
        print("⚠️ Invalid input. Using default delay of 20 seconds.")
        delay_seconds = 20.0

    full_url = f"{protocol}://{domain}"
    if not is_valid_url(full_url):
        print("[!] Invalid domain or protocol.")
        return

    print(f"\n[•] Starting scan: {full_url} with delay {delay_seconds} seconds")
    crawl(full_url, delay_seconds, base_domain=get_domain(full_url))
    save_to_file(full_url)

if __name__ == "__main__":
    main()

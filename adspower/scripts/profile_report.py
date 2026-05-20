#!/usr/bin/env python3
"""
AdsPower Profile Report Generator
===================================
Generates a CSV report of all browser profiles with their configuration status.
Useful for auditing proxy coverage, group distribution, and profile health.

Usage:
    python profile_report.py
    python profile_report.py --group "My Campaign"
    python profile_report.py --output my_report.csv

Output columns:
    profile_id, name, group, proxy_type, proxy_host, proxy_port, 
    created_at, last_open_time, has_proxy, has_cookie

Requirements:
    pip install requests python-dotenv
"""

import argparse
import csv
import os
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ADSPOWER_API_KEY", "")
BASE_URL = os.getenv("ADSPOWER_API_BASE", "http://local.adspower.net:50325")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def fetch_all_profiles(group_name=None):
    """Fetch all profiles with pagination."""
    all_profiles = []
    page = 1

    while True:
        params = {"page": page, "page_size": 100}
        if group_name:
            params["group_name"] = group_name

        resp = requests.get(
            f"{BASE_URL}/api/v1/user/list",
            headers=HEADERS,
            params=params,
            timeout=15,
        ).json()

        if resp["code"] != 0:
            print(f"[ERROR] {resp['msg']}")
            break

        profiles = resp["data"]["list"]
        if not profiles:
            break

        all_profiles.extend(profiles)
        page += 1
        time.sleep(0.5)  # Rate limit

    return all_profiles


def generate_report(profiles, output_file):
    """Generate a CSV report from profile data."""
    fieldnames = [
        "profile_id",
        "name",
        "group_name",
        "proxy_type",
        "proxy_host",
        "proxy_port",
        "created_at",
        "last_open_time",
        "has_proxy",
        "has_cookie",
    ]

    # Stats
    total = len(profiles)
    with_proxy = 0
    without_proxy = 0
    groups = {}

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p in profiles:
            proxy_config = p.get("user_proxy_config", {}) or {}
            proxy_host = proxy_config.get("proxy_host", "")
            has_proxy = bool(proxy_host)

            if has_proxy:
                with_proxy += 1
            else:
                without_proxy += 1

            group = p.get("group_name", "Default")
            groups[group] = groups.get(group, 0) + 1

            row = {
                "profile_id": p.get("user_id", ""),
                "name": p.get("name", ""),
                "group_name": group,
                "proxy_type": proxy_config.get("proxy_type", ""),
                "proxy_host": proxy_host,
                "proxy_port": proxy_config.get("proxy_port", ""),
                "created_at": p.get("created_time", ""),
                "last_open_time": p.get("last_open_time", ""),
                "has_proxy": "Yes" if has_proxy else "No",
                "has_cookie": "Yes" if p.get("cookie") else "No",
            }
            writer.writerow(row)

    # Print summary
    print(f"\n{'=' * 50}")
    print(f"  AdsPower Profile Report")
    print(f"{'=' * 50}")
    print(f"  Total profiles:    {total}")
    print(f"  With proxy:        {with_proxy}")
    print(f"  Without proxy:     {without_proxy}")
    print(f"  Groups:            {len(groups)}")
    for g, count in sorted(groups.items(), key=lambda x: -x[1]):
        print(f"    {g}: {count}")
    print(f"{'=' * 50}")
    print(f"  Report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate AdsPower profile report")
    parser.add_argument("--group", default=None, help="Filter by group name")
    parser.add_argument("--output", default="profile_report.csv", help="Output CSV file")
    args = parser.parse_args()

    if not API_KEY:
        print("[ERROR] Set ADSPOWER_API_KEY in your .env file")
        sys.exit(1)

    # Check API
    try:
        r = requests.get(f"{BASE_URL}/api/v1/status", headers=HEADERS, timeout=5)
        if r.json().get("code") != 0:
            print("[ERROR] API not ready")
            sys.exit(1)
    except Exception:
        print("[ERROR] Cannot connect to AdsPower. Is it running?")
        sys.exit(1)

    print("[...] Fetching profiles...")
    profiles = fetch_all_profiles(args.group)

    if not profiles:
        print("[ERROR] No profiles found")
        sys.exit(1)

    generate_report(profiles, args.output)


if __name__ == "__main__":
    main()

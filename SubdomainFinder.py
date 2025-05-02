import subprocess
import requests
import json
import os
import sys

def run_command(cmd, output_file):
    with open(output_file, "w") as out:
        subprocess.run(cmd, stdout=out, stderr=subprocess.DEVNULL)

def get_crtsh_subdomains(domain):
    print("[+] Gathering subdomains from crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=30)
        if response.ok:
            data = response.json()
            subdomains = set()
            for item in data:
                names = item.get("name_value", "").split("\n")
                for name in names:
                    subdomains.add(name.replace("*.","").strip())
            return sorted(subdomains)
        else:
            print("[!] crt.sh returned error.")
    except Exception as e:
        print(f"[!] Error querying crt.sh: {e}")
    return []
    
def get_certspotter_subdomains(domain):
    print("[+] Gathering subdomains from CertSpotter API...")
    url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"
    try:
        response = requests.get(url, timeout=30)
        if response.ok:
            data = response.json()
            subdomains = set()
            for item in data:
                for name in item.get("dns_names", []):
                    if domain in name:
                        subdomains.add(name.replace("*.", "").strip())
            return sorted(subdomains)
        else:
            print(f"[!] CertSpotter returned HTTP {response.status_code}")
    except Exception as e:
        print(f"[!] Error querying CertSpotter: {e}")
    return []

def write_list_to_file(filename, items):
    with open(filename, "w") as f:
        for item in sorted(set(items)):
            f.write(item + "\n")

def main(domain):
    out_dir = f"results_{domain}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"[*] Starting subdomain enumeration for {domain}")

    # Subfinder
    print("[+] Running subfinder...")
    subfinder_out = os.path.join(out_dir, "subfinder.txt")
    run_command(["subfinder", "-d", domain, "-silent"], subfinder_out)

    # crt.sh
    crtsh_subdomains = get_crtsh_subdomains(domain)
    crtsh_out = os.path.join(out_dir, "crtsh.txt")
    write_list_to_file(crtsh_out, crtsh_subdomains)

    #certspotter
    certspotter_subdomains = get_certspotter_subdomains(domain)
    certspotter_out = os.path.join(out_dir, "certspotter.txt")
    write_list_to_file(certspotter_out, certspotter_subdomains)

    # Combine
    print("[+] Combining and deduplicating...")
    with open(subfinder_out) as f:
        subfinder_subs = set(line.strip() for line in f)
    all_subs = sorted(set(subfinder_subs).union(set(crtsh_subdomains).union(set(certspotter_subdomains))))
    all_out = os.path.join(out_dir, "all.txt")
    write_list_to_file(all_out, all_subs)

    # Resolve with dnsx
    print("[+] Resolving subdomains with dnsx...")
    resolved_out = os.path.join(out_dir, "resolved.txt")
    run_command(["dnsx", "-silent", "-l", all_out], resolved_out)

    # Probe HTTP with httpx
    print("[+] Probing HTTP services with httpx...")
    httpx_out = os.path.join(out_dir, "active_http.txt")
    run_command(["httpx", "-silent", "-l", resolved_out], httpx_out)

    print(f"[✓] Done. Results saved in: {out_dir}/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python subdomain_enum.py example.com")
        print("Usage: Made BY HAkoorababa")
        sys.exit(1)
    main(sys.argv[1])

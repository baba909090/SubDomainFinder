#A Python script for subdomain enumeration using:-
  Subfinder:- (https://github.com/projectdiscovery/subfinder)
  crt.sh:- (https://crt.sh)
  CertSpotter:- (https://sslmate.com/labs/certspotter/)
  dnsx:- (https://github.com/projectdiscovery/dnsx)
  httpx:- (https://github.com/projectdiscovery/httpx)
  
#External tools
  subfinder
  dnsx
  httpx
  
#These are Go-based tools, so you'll need Go installed first. Download it from:
  https://go.dev/dl

#By default, Go installs tools in:
  C:\Users\<YourUsername>\go\bin
  This installs the tools to your Go/bin directory.
  Add Go/Bin to Windows PATH

#Then open PowerShell or Command Prompt and run:
  go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
  go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
  go install github.com/projectdiscovery/httpx/cmd/httpx@latest

#Verify Installation
In a new PowerShell window, run:
  subfinder -h
  dnsx -h
  httpx -h

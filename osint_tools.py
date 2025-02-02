import whois
import requests

# Get WHOIS information for a domain
def get_whois_info(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        return f"Error retrieving WHOIS data: {str(e)}"

# Perform an IP geolocation lookup
def ip_geolocation(ip):
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url)
    return response.json()

import requests

def get_country_from_ip(ip_address):
    url = f"https://api.country.is/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('country')
    else:
        print(f"Failed to fetch country for IP {ip_address}. Error: {response.status_code}")

# Test the function
ip_address = "9.9.9.9"
country = get_country_from_ip(ip_address)
if country:
    print(f"The country for IP address {ip_address} is {country}.")

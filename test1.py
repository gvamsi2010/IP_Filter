import requests

def get_ipv4_prefixes_for_country(country_code, date):
    url = f"https://stat.ripe.net/data/country-resource-list/data.json?resource={country_code}&time={date}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ipv4_prefixes = data.get('data', {}).get('resources', {}).get('ipv4')
        if ipv4_prefixes:
            # Sort the IPv4 prefixes
            sorted_ipv4_prefixes = sorted(ipv4_prefixes)
            return sorted_ipv4_prefixes
        else:
            return None
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None

def save_to_text_file(ipv4_prefixes, file_path):
    with open(file_path, 'w') as file:
        if ipv4_prefixes:
            file.write("Sorted IPv4 prefixes:\n")
            for prefix in ipv4_prefixes:
                file.write(prefix + '\n')
            print(f"IPv4 prefixes saved to {file_path}")
        else:
            file.write("No IPv4 prefixes found for the specified country and date.")
            print("No IPv4 prefixes found for the specified country and date.")

# Example usage:
country_code = 'at'  # Country code for Austria
date = '2020-12-01'
ipv4_prefixes = get_ipv4_prefixes_for_country(country_code, date)
if ipv4_prefixes:
    save_to_text_file(ipv4_prefixes, 'ipv4_prefixes.txt')

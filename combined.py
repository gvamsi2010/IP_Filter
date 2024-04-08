import boto3
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

def create_managed_prefix_list(prefixes, prefix_list_name, region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.create_managed_prefix_list(
        PrefixListName=prefix_list_name,
        Entries=[{'Cidr': prefix} for prefix in prefixes],
        MaxEntries=10000,
        TagSpecifications=[
            {
                'ResourceType': 'managed-prefix-list',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': prefix_list_name
                    },
                ]
            },
        ]
    )
    prefix_list_id = response['PrefixList']['PrefixListId']
    print(f"Managed Prefix List created with ID: {prefix_list_id}")
    return prefix_list_id

# Example usage:
country_code = 'at'  # Country code for Austria
date = '2020-12-01'
prefix_list_name = 'BlockedPrefixList'
region = 'us-west-1'  # Update with your desired region

ipv4_prefixes = get_ipv4_prefixes_for_country(country_code, date)
if ipv4_prefixes:
    prefix_list_id = create_managed_prefix_list(ipv4_prefixes, prefix_list_name, region)
else:
    print("No IPv4 prefixes found for the specified country and date.")

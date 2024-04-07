import json
import boto3
import requests

def lambda_handler(event, context):
    # Define the banned countries list
    banned_countries = ['RU', 'UA', 'CN', 'KP', 'IR', 'IQ', 'TR', 'TW']
    
    # Extract the IP address from the event
    ip_address = event['ip_address']
    
    # Call the Country API to get the country of the IP address
    response = requests.get(f'https://api.country.is/{ip_address}')
    
    # Check if the API call was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the country from the geolocation data
        country_code = data['country']
        
        # Check if the country code is in the banned countries list
        if country_code in banned_countries:
            # Add the IP address to the AWS managed prefix list
            ec2_client = boto3.client('ec2')
            response = ec2_client.modify_managed_prefix_list(
                PrefixListId='YOUR_PREFIX_LIST_ID',
                AddEntries=[
                    {
                        'Cidr': f"{ip_address}/32"
                    },
                ]
            )
            
            # Check if the IP was successfully added to the prefix list
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f"IP {ip_address} from {country_code} added to the managed prefix list.")
            else:
                print(f"Failed to add IP {ip_address} from {country_code} to the managed prefix list.")
        else:
            print(f"IP {ip_address} from {country_code} is not from a banned country.")
    else:
        print("Failed to fetch geolocation data for the IP address.")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully')
    }

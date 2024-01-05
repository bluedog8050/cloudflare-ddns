import requests
import json
import yaml
import datetime

def what_is_my_ip():
    """
    Returns the current public IP address.

    Returns:
        str: The current public IP address.
    """
    response = requests.get("https://api.ipify.org?format=json")
    
    if response.status_code == 200:
        return response.json()["ip"]
    else:
        return None

def update_dns_records():
    """
    Updates the DNS records on Cloudflare if the IP address has changed.

    Reads the configuration from a YAML file and retrieves the current IP address.
    Then, it fetches the DNS records from Cloudflare and compares them with the current IP.
    If the IP address has changed, it updates the corresponding DNS records with the new IP.

    Returns:
        None
    """
# warn and exit if config not found
    try:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("Config file not found. Please create a config.yaml file.")
        exit()

    API_TOKEN = config["API_TOKEN"]
    API_EMAIL = config["API_EMAIL"]
    ZONE_ID = config["ZONE_ID"]
    DNS_RECORDS = config["DNS_RECORDS"]

    # Get current IP address throw an exception if it fails
    current_ip = what_is_my_ip()
    if current_ip is None:
        raise Exception("Failed to get current IP address")

    # Get DNS records
    headers = {
        "X-Auth-Email": API_EMAIL,
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    response = requests.get(url, headers=headers)

    if response.json()['errors']:
        raise Exception(f"Failed to retrieve DNS records. Error: {response.json()['errors'][0]['message']}")

    dns_records = response.json()["result"]

    # If response status code is not 200, raise an exception
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve DNS records. Response code: {response.status_code}")

    # Update DNS records if IP is different
    for record in dns_records:
        if record["type"] == "A" and record["name"] in DNS_RECORDS and record["content"] != current_ip:
            record_id = record["id"]
            record["content"] = current_ip
            update_url = f"{url}/{record_id}"
            response = requests.put(update_url, headers=headers, data=json.dumps(record))
            if response.status_code == 200:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Updated DNS record {record['name']} with IP {current_ip}")
            else:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Failed to update DNS record {record['name']}")

#run the update_dns_records function if the script is run directly
if __name__ == "__main__": update_dns_records()

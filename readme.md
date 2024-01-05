Updates the DNS records on Cloudflare if the IP address has changed.

    The script reads the configuration from a YAML file including what domain A records to check 
    and retrieves the current IP address.
    Then, it fetches the DNS records from Cloudflare and compares them with the current IP.
    If the IP address has changed, it updates the corresponding DNS records with the new IP.

__Setup__
1. Open config.yaml.example and replace the plalceholders with your cloudflare account and zone information
2. Rename or copy the config.yaml.example to config.yaml
3. Install python dependencies with ```pip install -r requirements.txt```
4. Run the script with ```python3 cloudflare-ddns.py``` to make sure your configuration works
5. Add the previous command to your scheduler of choice to run every minute. Changes will only be sent to cloudflare if the A records of the dns records you chose to update are different from your machines current wan IP.

__To find your Zone ID:__
1. Login to Cloudflare:
    * Open your web browser and go to the Cloudflare website.
    Log in to your Cloudflare account.
    Access the Dashboard:
    * After logging in, you should be on the Cloudflare dashboard.
2. Select the Domain:
    * From the dashboard, select the domain for which you want to find the Zone ID.
3. Copy your Zone ID:
    * On the right panel of your domain overview, find the API section which should have your zone id listed
    * Copy the zone id to the config file of this app

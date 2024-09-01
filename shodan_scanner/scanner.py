import psutil
import ipaddress
import socket
import shodan
import csv
from shodan import APIError
#please note bulk lookup works only with corporate plan

class Scanner:
    def __init__(self, api_key):
        self.api = shodan.Shodan(api_key)

    def get_ip_range(self):
        # Get all network interfaces and their IP addresses
        addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in addrs.items():
            if interface_name == 'lo':  # Skip the loopback interface
                continue
            for address in interface_addresses:
                if address.family == socket.AF_INET:  # Check if the address is an IPv4 address
                    ip_address = address.address
                    if ip_address.startswith("127."):  # Skip local addresses
                        continue
                    # Assuming /24 subnet for simplicity
                    ip_network = ipaddress.ip_network(f"{ip_address}/24", strict=False)
                    ip_range = str(ip_network)
                    print(f"Detected IP range {ip_range} using interface {interface_name}")
                    return ip_range

        print("Failed to detect IP range. Please check your network settings.")
        return None

    def scan_network(self, ip_range, output_filename='shodan_scan_results.csv'):
        try:
            # Perform a Shodan search on the given IP range
            results = self.api.search(f'net:{ip_range}')

            print(f'Results found: {results["total"]}')

            # Open a CSV file to write the results
            with open(output_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header row
                writer.writerow(['IP', 'Port', 'Hostnames', 'OS', 'Timestamp'])

                # Extract useful information from the results
                for result in results['matches']:
                    writer.writerow([
                        result['ip_str'],
                        result['port'],
                        ','.join(result.get('hostnames', ['None'])),
                        result.get('os', 'Unknown'),
                        result['timestamp']
                    ])

            print(f'Results saved to {output_filename}')

        except APIError as e:
            print(f'Error: {e}')


def main():
    # Replace 'YOUR_SHODAN_API_KEY' with your actual Shodan API key
    api_key = 'ccc'

    # Create a Scanner instance
    scanner = Scanner(api_key)

    # Automatically get the IP range of your current network interface
    ip_range = "8.8.8.8"#scanner.get_ip_range()

    if ip_range:
        print(f"Scanning IP range: {ip_range}")

        # Perform the scan and save the results to a CSV file
        scanner.scan_network(ip_range)
    else:
        print("Failed to get IP range. Please check your network interface.")



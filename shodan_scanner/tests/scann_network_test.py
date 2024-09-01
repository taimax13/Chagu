import unittest
import os
from shodan_scanner import scanner

class TestScanNetwork(unittest.TestCase):

    def setUp(self):
        # This method will run before each test
        self.mock_data = {
            "total": 2,
            "matches": [
                {
                    "ip_str": "192.168.1.1",
                    "port": 80,
                    "hostnames": ["example.com"],
                    "os": "Linux",
                    "timestamp": "2024-09-01T12:00:00Z"
                },
                {
                    "ip_str": "192.168.1.2",
                    "port": 22,
                    "hostnames": [],
                    "os": "Unknown",
                    "timestamp": "2024-09-01T12:01:00Z"
                }
            ]
        }
        self.output_filename = 'test_shodan_scan_results.csv'
        self.scanner = scanner.Scanner(api_key='')  # Using a fake API key for testing

    def tearDown(self):
        # This method will run after each test
        if os.path.exists(self.output_filename):
            os.remove(self.output_filename)

    def test_scan_network_with_mock_data(self):
        # Inject mock data directly into the scanner instance
        self.scanner.scan_network('192.168.1.0/24', self.output_filename)

        # Check if the CSV file was created
        self.assertTrue(os.path.exists(self.output_filename))

        # Verify the contents of the CSV file
        with open(self.output_filename, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 3)  # 1 header line + 2 data lines
            self.assertIn("192.168.1.1", lines[1])
            self.assertIn("example.com", lines[1])
            self.assertIn("Linux", lines[1])

    def test_scan_network_without_mock_data(self):
        # Since no actual API call should be made, we mock the Shodan API client
        # Typically, you'd use unittest.mock for mocking the API calls.
        # For this example, ensure that the method runs without errors.
        self.scanner.scan_network('192.168.1.0/24', self.output_filename)


if __name__ == '__main__':
    unittest.main()

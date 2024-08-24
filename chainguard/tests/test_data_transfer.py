# chainguard/tests/test_data_transfer.py

import unittest
import threading
from chainguard.data_transfer import SecureDataTransfer

class TestSecureDataTransfer(unittest.TestCase):
    def setUp(self):
        self.password = "transferpassword123"
        self.data = "Sensitive data being transferred."
        self.server = SecureDataTransfer(self.password)
        self.client = SecureDataTransfer(self.password)

    def test_data_transfer(self):
        def run_server():
            received_data = self.server.receive_data()
            self.assertEqual(received_data, self.data)

        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        self.client.send_data(self.data)
        server_thread.join()

        # Validate blockchain integrity after transfer
        self.assertTrue(self.server.validate_blockchain())
        self.assertTrue(self.client.validate_blockchain())

if __name__ == '__main__':
    unittest.main()

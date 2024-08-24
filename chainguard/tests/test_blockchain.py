import unittest
from chainguard.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block.data, "Genesis Block")

    def test_add_block(self):
        self.blockchain.add_block("Test Block")
        latest_block = self.blockchain.get_latest_block()
        self.assertEqual(latest_block.data, "Test Block")

    def test_chain_validity(self):
        self.blockchain.add_block("First block")
        self.blockchain.add_block("Second block")
        self.assertTrue(self.blockchain.is_chain_valid())

    def test_chain_invalidity(self):
        self.blockchain.add_block("First block")
        self.blockchain.chain[1].data = "Tampered Data"
        self.assertFalse(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()


from chainguard.blockchain import Blockchain

class BlockchainLogger:
    def __init__(self):
        self.blockchain = Blockchain()

    def log_data(self, data: str):
        """
        Logs the provided data into the blockchain.
        Args:
            data (str): The data to be logged in the blockchain.
        Returns:
            dict: The details of the newly added block.
        """
        new_block = self.blockchain.add_block(data)
        return {
            "block_hash": new_block.hash,
            "block_index": new_block.index,
            "blockchain_length": len(self.blockchain.chain),
            "previous_hash": new_block.previous_hash,
            "timestamp": new_block.timestamp
        }

    def is_blockchain_valid(self):
        """
        Validates the integrity of the blockchain.
        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        return self.blockchain.is_chain_valid()

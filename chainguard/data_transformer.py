from chainguard.blockchain_logger import BlockchainLogger

class DataTransformer:
    def __init__(self):
        """
        Initializes a DataTransformer with a blockchain logger instance.
        """
        self.blockchain_logger = BlockchainLogger()

    def secure_transform(self, data):
        """
        Securely transforms the input data by logging it into the blockchain.

        Args:
            data (dict): The log data or any data to be securely transformed.

        Returns:
            dict: A dictionary containing the original data, block hash, and blockchain length.
        """
        # Log the data into the blockchain
        block_details = self.blockchain_logger.log_data(data)

        # Return the block details and blockchain status
        return {
            "data": data,
            **block_details
        }

    def validate_blockchain(self):
        """
        Validates the integrity of the blockchain.
        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        return self.blockchain_logger.is_blockchain_valid()

import socket
from chainguard.encryption import AESCipher
from chainguard.blockchain_logger import BlockchainLogger

class SecureDataTransfer:
    def __init__(self, password: str, host: str = 'localhost', port: int = 12345):
        self.cipher = AESCipher(password)
        self.host = host
        self.port = port
        self.blockchain_logger = BlockchainLogger()

    def send_data(self, data: str):
        """
        Encrypts and sends data over the network, then logs it in the blockchain.
        """
        encrypted_data = self.cipher.encrypt(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(encrypted_data.encode())
            print(f"Sent encrypted data: {encrypted_data}")
            # Log the transaction in the blockchain
            self.blockchain_logger.log_data(encrypted_data)

    def receive_data(self):
        """
        Receives encrypted data, decrypts it, and logs it in the blockchain.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                encrypted_data = conn.recv(1024).decode()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                print(f"Received encrypted data: {encrypted_data}")
                print(f"Decrypted data: {decrypted_data}")
                # Log the transaction in the blockchain
                self.blockchain_logger.log_data(encrypted_data)
                return decrypted_data

    def validate_blockchain(self):
        """
        Validates the blockchain's integrity.
        """
        return self.blockchain_logger.is_blockchain_valid()

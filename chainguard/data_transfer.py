# chainguard/data_transfer.py

import socket
from chainguard.encryption import AESCipher
from chainguard.blockchain import Blockchain

class SecureDataTransfer:
    def __init__(self, password: str, host: str = 'localhost', port: int = 12345):
        self.cipher = AESCipher(password)
        self.host = host
        self.port = port
        self.blockchain = Blockchain()

    def send_data(self, data: str):
        encrypted_data = self.cipher.encrypt(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(encrypted_data.encode())
            print(f"Sent encrypted data: {encrypted_data}")
            # Log the transaction in the blockchain
            self.blockchain.add_block(encrypted_data)

    def receive_data(self):
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
                self.blockchain.add_block(encrypted_data)
                return decrypted_data

    def validate_blockchain(self):
        return self.blockchain.is_chain_valid()

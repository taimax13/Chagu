# Chagu 
# ChainGuard

ChainGuard is a custom protocol designed for secure data transformation using blockchain technology. It leverages AES encryption for confidentiality and plans to integrate blockchain for data integrity and traceability.

## Features
- AES Encryption and Decryption
- (Planned) Blockchain Integration
- Unit and Integration Tests

## Installation

```bash
pip install -r requirements.txt
```
usage
``` code
    from chainguard.encryption import AESCipher
    
    password = "yourpassword"
    cipher = AESCipher(password)
    
    # Encrypt and Decrypt
    plaintext = "Hello, World!"
    encrypted = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

```
## Data Transfer Protocol

ChainGuard now includes a secure data transfer protocol to securely send and receive data between nodes.

### Example Usage

```python
from chainguard.data_transfer import SecureDataTransfer

# Initialize SecureDataTransfer with a shared password
transfer = SecureDataTransfer(password="securepassword")

# On the sending side
transfer.send_data("This is a secure message")

# On the receiving side
transfer.receive_data()
```


## Blockchain Integration

ChainGuard includes a custom blockchain to securely log and verify each data transfer. This ensures transparency, immutability, and traceability of all transactions.

### Example Usage

```python
from chainguard.data_transfer import SecureDataTransfer

# Initialize SecureDataTransfer with a shared password
transfer = SecureDataTransfer(password="securepassword")

# On the sending side
transfer.send_data("This is a secure message")

# On the receiving side
transfer.receive_data()

# Validate blockchain
is_valid = transfer.validate_blockchain()
print(f"Blockchain valid: {is_valid}")
```

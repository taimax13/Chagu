import unittest
from chainguard.encryption import AESCipher


class TestAESCipher(unittest.TestCase):
    def setUp(self):
        self.password = "securepassword123"
        self.cipher = AESCipher(self.password)

    def test_encryption_decryption(self):
        plaintext = "This is a secret message."
        encrypted = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(encrypted)

        self.assertEqual(plaintext, decrypted)

    def test_different_plaintext(self):
        plaintext1 = "Message One"
        plaintext2 = "Message Two"
        encrypted1 = self.cipher.encrypt(plaintext1)
        encrypted2 = self.cipher.encrypt(plaintext2)

        self.assertNotEqual(encrypted1, encrypted2)
        self.assertEqual(self.cipher.decrypt(encrypted1), plaintext1)
        self.assertEqual(self.cipher.decrypt(encrypted2), plaintext2)


if __name__ == '__main__':
    unittest.main()

from .hash_iterator import HashIterator
from hashlib import sha256

__all__ = ["IterSHA256"]

def validateIterSHA256(key: int, num_keys: int):
    if key < 0:
        raise TypeError("key must be non negative")
    if num_keys <= 0:
        raise TypeError("num_keys must be positive")

class IterSHA256(HashIterator):
    
    def __init__(self, key: int, num_keys: int):
        validateIterSHA256(key, num_keys)
        super().__init__(key.to_bytes(key.bit_length(), byteorder='big'))
        self.range = key + num_keys

    def generate_hash(self, nonce: bytes):
        h = sha256()
        h.update(nonce)
        return h.hexdigest()

    def check_bounds(self, nonce: bytes):
        value = int.from_bytes(nonce, byteorder='big')
        return value >= self.range

    def increment(self, nonce: bytes):
        value = int.from_bytes(nonce, byteorder='big')
        value += 1
        return value.to_bytes(value.bit_length(), byteorder='big')
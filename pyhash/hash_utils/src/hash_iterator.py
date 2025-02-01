from abc import ABC, abstractmethod

__all__ = ["HashIterator"]

class HashIterator(ABC):

    def __init__(self, nonce: bytes):
        self.__nonce = nonce
        self.__key = None
        self.__hexdigest = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.__check_nonce():
            raise StopIteration
        else:
            self.__hexdigest = self.generate_hash(self.__nonce)    
            self.__key = self.__nonce
            self.__increment_nonce()
            return self.__hexdigest

    def __check_nonce(self):
        return self.check_bounds(self.__nonce)

    def __increment_nonce(self):
        self.__nonce = self.increment(self.__nonce)

    def key(self):
        return int.from_bytes(self.__key, byteorder='big')

    def hexdigest(self):
        return self.__hexdigest

    @abstractmethod
    def generate_hash(self, nonce: bytes) -> str:
        pass

    @abstractmethod
    def check_bounds(self, nonce: bytes) -> bool:
        pass

    @abstractmethod
    def increment(self, nonce: bytes) -> None:
        pass

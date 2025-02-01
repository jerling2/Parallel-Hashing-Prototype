from abc import ABC, abstractmethod

__all__ = ["HashIterator"]

class HashIterator(ABC):

    def __init__(self, nonce: bytes):
        self.__nonce = nonce
        self.__key = None

    def __iter__(self):
        return self

    def __next__(self):
        if __check_nonce():
            raise StopIteration
        else:
            h = generate_hash(nonce)
            self.__key = nonce
            self.__increment_nonce()
            return h

    def __check_nonce(self):
        return self.bound_nonce()

    def __increment_nonce(self):
        self.__nonce = increment(self.__nonce)

    def key(self) -> bytes:
        return self.__key

    @abstractmethod
    def generate_hash(self, nonce: bytes) -> str:
        pass

    @abstractmethod
    def check_bounds(self, nonce: bytes) -> bool:
        pass

    @abstractmethod
    def increment(self, nonce: bytes) -> None:
        pass



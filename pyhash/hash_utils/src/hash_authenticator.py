import sys
from .hash_iterator import HashIterator

__all__ = ["HashAuthenticator"]

class HashAuthenticator:
    
    def __init__(self, callback):
        self.callback = callback
        self.solution = {'key': None, 'hexdigest': None}
        self._iterators = []

    def add_iterator(self, iterator):
        if isinstance(iterator, HashIterator):
            self._iterators.append(iterator)
        else:
            raise TypeError("iterator is not an HashIterator")

    def remove_iterator(self, index: int):
        self._iterators.pop(index)

    def __worker(self, index, iterator):
        try:
            hexdigest = next(iterator)
            if self.callback(hexdigest) is True:
                self._raise_solution(iterator.key(), hexdigest)
        except StopIteration:
            self.remove_iterator(index)
        except Exception as e:
            print(f"Worker {index} encountered an unexpected error: {e}")
            self.remove_iterator(index)

    def _raise_solution(self, key, hexdigest):
        self.solution['key'] = key
        self.solution['hexdigest'] = hexdigest
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            for index, iterator in enumerate(self._iterators):
                self.__worker(index, iterator)
                if not self._running:
                    break
            if not self._iterators:
                self._running = False
__all__ = ["HashWorker"]

class HashWorker:

    def __init__(self, callback, iterator):
        self.callback = callback
        self.iterator = iterator

    def run(self):
        for hexdigest in self.iterator:
            if self.callback(hexdigest):
                return {'key': self.iterator.key(), 'hexdigest': hexdigest}
        return {'key': None, 'hexdigest': None}
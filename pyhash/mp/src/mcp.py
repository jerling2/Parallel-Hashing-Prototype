from .worker import HashWorker
from dask.distributed import Client, as_completed

class MCP:
    
    def __init__(self, num_workers, constraint, chunk_size, iteratorClass):
        self.client = Client(n_workers=num_workers, threads_per_worker=1)
        self.num_workers = num_workers
        self.constraint = constraint
        self.iteratorClass = iteratorClass
        self.chunk_size = chunk_size
        self.__next_index = 0

    def __new_worker(self):
        start_key = self.__next_index * self.chunk_size
        num_keys = self.chunk_size
        iterator = self.iteratorClass(start_key, num_keys)
        self.__next_index += 1
        return HashWorker(self.constraint, iterator)

    def run(self):
        workers = [self.__new_worker() for _ in range(self.num_workers)]
        futures = {self.client.submit(w.run) for w in workers}
        ac = as_completed(futures)
        for future in ac:
            result = future.result()
            if result['key'] is None:
                new_worker = self.__new_worker()
                new_future = self.client.submit(new_worker.run)
                futures.add(new_future)
                ac.add(new_future)
            else:
                for remaining_future in futures:
                    remaining_future.cancel()
                return result

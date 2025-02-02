import os
import sys
import unittest
import signal
import time

# Define a timeout exception handler
def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out")

# Register the signal handler
signal.signal(signal.SIGALRM, timeout_handler)

# Add our pyhash package to PATH
current_directory = os.path.dirname(os.path.realpath(__file__))           # pwd
parent_directory = os.path.dirname(current_directory)                   # cd ..
parent_directory = os.path.dirname(parent_directory)                    # cd ..
parent_directory = os.path.dirname(parent_directory)                    # cd ..
sys.path.append(parent_directory)  

from pyhash import mp, hash_utils

class TestHashUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ This runs before all tests """
        cls.__num_failures = 0
        cls.__num_errors = 0
        cls.__num_passes = 0
        print('\x1B[1;34mRunning Unit Tests for mp Package\x1b[0m')

    @classmethod
    def tearDownClass(cls):
        """ This runs after all tests """
        total = cls.__num_failures + cls.__num_errors + cls.__num_passes
        print(f"Score: {cls.__num_passes} / {total}", end="\t", file=sys.stderr)
        print(f"Failed: {cls.__num_failures}", end="\t", file=sys.stderr)
        print(f"Errors: {cls.__num_errors}", file=sys.stderr)

    def setUp(self):
        """ This runs before each test """
        print(f"[{self._testMethodName}]...", end="", file=sys.stderr)

    def tearDown(self):
        """ This runs after each test """
        if self._outcome.result.errors:
            TestHashUtils.__num_errors += 1
            print("ERROR", file=sys.stderr)
        elif self._outcome.result.failures:
            TestHashUtils.__num_failures += 1
            print("FAIL", file=sys.stderr)
        else:
            TestHashUtils.__num_passes += 1
            print("PASS", file=sys.stderr)

    def test_01_HashWorker(self):
        """ Run a Single Hash Worker """
        it = hash_utils.IterSHA256(0, 100)
        cb = lambda x: x.endswith('1')
        worker = mp.HashWorker(cb, it)
        result = worker.run()
        self.assertIsNotNone(result['key'])
        self.assertIsNotNone(result['hexdigest'])

    def test_02_MCP(self):
        constraint = lambda x: x.endswith('ffff')
        mcp = mp.MCP(4, constraint, 100, hash_utils.IterSHA256)
        signal.alarm(20) # signal an alarm for 20 seconds
        try: 
            result = mcp.run()
        except TimeoutError:
            self.fail("MCP took too long")
        except Exception as e:
            self.fail(f"MCP encounted an unexpected error: {e}")
        self.assertIsNotNone(result['key'])
        self.assertIsNotNone(result['hexdigest'])
        self.assertTrue(constraint(result['hexdigest']))

if __name__ == "__main__":
    unittest.main(verbosity=0)
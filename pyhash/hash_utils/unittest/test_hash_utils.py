import os
import sys
import unittest

# Add our pyhash package to PATH
current_directory = os.path.dirname(os.path.realpath(__file__))           # pwd
parent_directory = os.path.dirname(current_directory)                   # cd ..
parent_directory = os.path.dirname(parent_directory)                    # cd ..
parent_directory = os.path.dirname(parent_directory)                    # cd ..
sys.path.append(parent_directory)  

from pyhash import hash_utils

class TestHashUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ This runs before all tests """
        cls.__num_failures = 0
        cls.__num_errors = 0
        cls.__num_passes = 0
        print('\x1B[1;34mRunning Unit Tests for hash_utils Package\x1b[0m')

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
    
    def test_01_abstract_HashIterator(self):
        """ Raises a TypeError because we cannot initialize an abstract class """
        with self.assertRaises(TypeError):
            h = hash_utils.HashIterator(b'nounce')

    def test_02_init_IterSHA256(self):
        """ Initialize a SHA256 Hash Iterarator. """
        hash_utils.IterSHA256(0, 10)

    def test_03_init_IterSHA256_error(self):
        """ Initialze a SHA256 Hash Iterarator with invalid parameters. """
        with self.assertRaises(TypeError):
            hash_utils.IterSHA256(-1, 1)
        with self.assertRaises(TypeError):
            hash_utils.IterSHA256(0, 0)

    def test_04_iterate_IterSHA256(self):
        hash_generator = hash_utils.IterSHA256(0, 10)
        output = []
        for digest in hash_generator:
            output.append(digest)
        self.assertEqual(len(output), 10)
        
    def test_05_init_HashAuthenticator(self):
        auth = hash_utils.HashAuthenticator(lambda x: True)

    def test_06_run_HashAuthenticator_with_one_iterator(self):
        """ 
        Find a key that produces a hexdigest ending with 1. The odds are about
        1 in 16 or a 6.25% chance. The authenticator runs one iterator.
        """
        constraint_ends_with_one = lambda x: x.endswith("1")
        auth = hash_utils.HashAuthenticator(constraint_ends_with_one)
        auth.add_iterator(hash_utils.IterSHA256(0, 100))
        auth.run()
        self.assertIsNotNone(auth.solution['key'])
        self.assertIsNotNone(auth.solution['hexdigest'])
        self.assertTrue(auth.solution['hexdigest'].endswith("1"))

    def test_07_run_HashAuthenticator_with_many_iterators(self):
        """ 
        Find a key that produces a hexdigest ending with ff. The odds are about
        1 in 256 or about a 0.4% chance. The authenticator runs many iterators.
        """
        constraint_ends_with_ff = lambda x: x.endswith("ff")
        auth = hash_utils.HashAuthenticator(constraint_ends_with_ff)
        # Attach 30 SHA256 iterators each with a key pool size of 100 to search
        # keys ranging from 0 to 3,000.
        allotment = 100
        for i in range(30):
            auth.add_iterator(hash_utils.IterSHA256(i*allotment, allotment))
        auth.run()
        self.assertIsNotNone(auth.solution['key'])
        self.assertIsNotNone(auth.solution['hexdigest'])
        self.assertTrue(auth.solution['hexdigest'].endswith("ff"))

if __name__ == "__main__":
    unittest.main(verbosity=0)
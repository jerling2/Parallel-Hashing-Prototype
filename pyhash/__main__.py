import re
from pyhash import *
import signal
import time
import logging

# Suppress Dask warnings by setting the log level to ERROR
# Used to supress the 'Removing worker ... caused the cluster to lose already
# computed task(s)' message.
logging.getLogger('distributed.worker.state_machine').setLevel(logging.ERROR)
logging.getLogger('distributed.scheduler').setLevel(logging.ERROR)

# Define a timeout exception handler
def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out")

# Register the signal handler
signal.signal(signal.SIGALRM, timeout_handler)

def user_input():
    # Ask for the characters the hexdigest should end with
    while True:
        hexdigest_end = input("What characters should the hexdigest end with? (default: c0ffee) ")
        if re.match("^[0-9a-fA-F]{1,64}$", hexdigest_end):
            hexdigest_constraint = lambda x: x.endswith(hexdigest_end.lower())
            hexdigest_string = hexdigest_end.lower()
            break
        else:
            hexdigest_constraint = lambda x: x.endswith('c0ffee')
            hexdigest_string = 'c0ffee'
            break
    while True:
        num_workers_string = input("How many workers? (default: 4) ")
        if num_workers_string == '':
            num_workers = 4
            break
        try:
            num_workers = int(num_workers_string)
            if num_workers <= 0:
                raise ValueError("The number of workers must be greater than zero.")
            break
        except ValueError as e:
            print(f"Invalid input! {e} Please enter a valid number.")
    while True:
        chunk_size_string = input("Chunk size? (default: 32768) ")
        if chunk_size_string == '':
            chunk_size = 32768
            break
        try:
            chunk_size = int(chunk_size_string)
            if chunk_size <= 0:
                raise ValueError("The chunk size must be greater than zero.")
            break
        except ValueError as e:
            print(f"Invalid input! {e} Please enter a valid number.")
    while True:
        timeout_string = input("Timeout (s)? (default: no timeout) ")
        if timeout_string == '':
            timeout = -1
            break
        try: 
            timeout = int(timeout_string)
            if timeout <= 0:
                raise ValueError("The timeout must be greater than zero.")
            break
        except ValueError as e:
            print(f"Invalid input! {e} Please enter a valid number.")
    return hexdigest_string, hexdigest_constraint, num_workers, chunk_size, timeout


def main():
    hexdigest_end, hexdigest_constraint, num_workers, chunk_size, timeout = user_input()
    
    mcp = mp.MCP(num_workers, hexdigest_constraint, chunk_size, hash_utils.IterSHA256)
    print(f"\x1B[1;95mRunning MCP (num_workers={num_workers} constraint='{hexdigest_end}', chunk_size={chunk_size}, hashIterator='SHA256')\x1b[0m")
    if timeout != -1:
        print(f"\x1b[2;35mTimeout in {timeout} (s)\x1b[0m")
        signal.alarm(timeout)
    else:
        print("\x1b[2;35mNo timeout\x1b[0m")
    try: 
        start_time = time.time()
        result = mcp.run()
        elapsed_time = time.time() - start_time
        print(result)
        print(f'\x1b[2;35mRan for \x1b[1m{elapsed_time:.4f} (s)\x1b[0m')
    except TimeoutError:
        print("\x1b[2;34mTimeout!\x1b[0m")
    except Exception as e:
        print(f"Uncaught error: {e}")

if __name__ == "__main__":
    main()
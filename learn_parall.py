import threading
from multiprocessing import Process as mp
from concurrent.futures import ProcessPoolExecutor
import timeit

def print_fib(n):
    """Prints the Fibonacci sequence up to the nth number."""
    def fib(n):
        """Returns the nth Fibonacci number."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    
    print(f"Fibonacci number {n}: {fib(n)}")  # Print the nth Fibonacci number

def test_threadings():
    n = 10  # Number of Fibonacci numbers to print
    start_time = timeit.default_timer()  # Start timing

    # Create a thread to run the Fibonacci function
    fib_thread_1 = threading.Thread(target=print_fib, args=(40,))
    fib_thread_2 = threading.Thread(target=print_fib, args=(41,))

    fib_thread_1.start()  # Start the thread
    fib_thread_2.start()  # Start the second thread

    fib_thread_1.join()  # Wait for the thread to finish
    fib_thread_2.join()

    elapsed_time = timeit.default_timer() - start_time  # Calculate elapsed time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")  # Print elapsed time

def test_processings():
    """Test function to demonstrate multiprocessing."""
    n = 10  # Number of Fibonacci numbers to print
    start_time = timeit.default_timer()  # Start timing

    # Create a process to run the Fibonacci function
    fib_process_1 = mp(target=print_fib, args=(40,))
    fib_process_2 = mp(target=print_fib, args=(41,))

    fib_process_1.start()  # Start the process
    fib_process_2.start()  # Start the second process

    fib_process_1.join()  # Wait for the process to finish
    fib_process_2.join()

    elapsed_time = timeit.default_timer() - start_time  # Calculate elapsed time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")  # Print elapsed time


def main():
    """Main function to run the threading test."""
    print("Starting threading test...")  # Indicate start of the test
    test_processings()  # Run the threading test
    print("Threading test completed.")  # Indicate completion of the test


if __name__ == "__main__":
    main()  # Run the main function
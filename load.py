import requests
import time
import random
import threading

# Target URL
url = 'http://35.85.44.18/'

def send_requests(thread_id):
    """
    Function that runs in each thread to send GET requests indefinitely.
    """
    while True:
        try:
            # Random interval between 2 and 2.5 seconds
            interval = random.uniform(2, 2.5)
            
            # Start timing the request
            start_time = time.time()

            # Send the GET request
            response = requests.get(url)

            # End timing the request
            end_time = time.time()

            # Calculate the duration of the request
            duration = end_time - start_time

            # Print the response text and the duration with thread ID
            print(f"[Thread {thread_id}] Response: {response.text}")
            print(f"[Thread {thread_id}] Request took {duration:.4f} seconds")

            # Calculate how much time to wait to maintain the interval
            time_to_wait = interval - duration

            # If the request was fast, wait the remaining time; otherwise, proceed immediately
            if time_to_wait > 0:
                time.sleep(time_to_wait)

        except requests.exceptions.RequestException as e:
            # Handle possible exceptions (like connection errors)
            print(f"[Thread {thread_id}] An error occurred: {e}")
            time.sleep(5)  # Wait for a bit before retrying

def main():
    while True:
        try:
            # Prompt the user to enter the number of threads
            num_threads = int(input("Enter the number of threads to run: "))
            if num_threads < 1:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    threads = []

    # Create and start the specified number of threads
    for i in range(1, num_threads + 1):
        thread = threading.Thread(target=send_requests, args=(i,), daemon=True)
        thread.start()
        threads.append(thread)
        print(f"Started Thread {i}")

    try:
        # Keep the main thread alive to allow daemon threads to run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all threads...")

if __name__ == "__main__":
    main()
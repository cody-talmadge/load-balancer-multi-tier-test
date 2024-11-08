import requests
import time
import random
import threading

# Cluster load balancer URL
url = 'http://AWS-Load-Balancer-1380354736.us-west-2.elb.amazonaws.com'

def send_requests(thread_id):
    while True:
        try:
            # Random interval between 2 and 2.5 seconds
            interval = random.uniform(2, 2.5)
            
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            duration = end_time - start_time

            print(f"[Thread {thread_id}] Response: {response.text}")
            print(f"[Thread {thread_id}] Request took {duration:.4f} seconds")

            time_to_wait = interval - duration
            if time_to_wait > 0:
                time.sleep(time_to_wait)

        except requests.exceptions.RequestException as e:
            print(f"[Thread {thread_id}] An error occurred: {e}")
            time.sleep(5)

def main():
    while True:
        try:
            num_threads = int(input("Enter the number of threads to run: "))
            if num_threads < 1:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    threads = []
    for i in range(1, num_threads + 1):
        thread = threading.Thread(target=send_requests, args=(i,), daemon=True)
        thread.start()
        threads.append(thread)
        print(f"Started Thread {i}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all threads...")

if __name__ == "__main__":
    main()
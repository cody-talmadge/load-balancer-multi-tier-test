import requests
import time
import random
import threading
import csv

# Cluster load balancer URL
# url = 'http://AWS-Load-Balancer-1380354736.us-west-2.elb.amazonaws.com'
url = 'http://35.184.71.99/'
request_times = []
stop_flag = False

def send_requests(thread_id):
    try:
        
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        duration = end_time - start_time

        response_data = response.json()
        server_ip = response_data.get('server_ip')
        request_times.append({'start time': start_time, 'duration': duration, 'server_ip': server_ip})

        # print(f"[Thread {thread_id}] Response: {response.text}")
        print(f"[Thread {thread_id}] [Server IP {server_ip}] Request took {duration:.4f} seconds")


    except requests.exceptions.RequestException as e:
        print(f"[Thread {thread_id}] An error occurred: {e}.")
        time.sleep(5)

def thread_scheduler(requests_per_second):
    global stop_flag
    interval_between_requests = 1.0 / requests_per_second
    request_count = 0
    while not stop_flag:
        request_count += 1
        thread_start_time = time.time()
        threading.Thread(target=send_requests, args=(request_count,), daemon=True).start()
        elapsed_time = time.time() - thread_start_time
        wait_time = interval_between_requests - elapsed_time
        if wait_time > 0:
            time.sleep(wait_time)


def save_data(filename):
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['Start Time', 'Duration', 'Server IP'])
        writer.writeheader()
        for result in request_times:
            writer.writerow({'Start Time': result['start time'], 'Duration': result['duration'], 'Server IP': result['server_ip']})

def main():
    requests_per_second = int(input("Enter the number of threads/requests per second: "))

    scheduler_thread = threading.Thread(target=thread_scheduler, args=(requests_per_second,), daemon=True)
    scheduler_thread.start()

    input("Press any key to stop sending requests and save data\n")
    global stop_flag
    stop_flag = True

    scheduler_thread.join()

    current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    save_data(current_time + '_request_times.csv')
    print(f"Results saved to {current_time + '_request_times.csv'}")


if __name__ == "__main__":
    main()
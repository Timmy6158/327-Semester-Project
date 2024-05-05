import requests
import random
import time
import threading
import logging
import socket

RESOURCE_NODE_HOST = "resourcenode"
RESOURCE_NODE_PORT = 5000
RESOURCE_NODE_ENDPOINT = "tasks"
NUM_REQUESTS = 100

# List to store response times
response_times = []

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def get_resource_node_url():
    # Use Docker DNS resolution to get the IP address of the resource node
    resource_node_ip = socket.gethostbyname(RESOURCE_NODE_HOST)
    return f"http://{resource_node_ip}:{RESOURCE_NODE_PORT}/{RESOURCE_NODE_ENDPOINT}"

RESOURCE_NODE_URL = get_resource_node_url()

class LockManager:
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self):
        """Acquire lock"""
        self.lock.acquire()

    def release(self):
        """Release lock"""
        self.lock.release()

lock_manager = LockManager()

def simulate_read_write_requests():
    start_time = time.time()
    for _ in range(NUM_REQUESTS):
        task = {
            "name": f"Task {random.randint(1, 100)}",
            "description": "Sample description"
        }

        request_start_time = time.time()

        lock_manager.acquire()

        if random.random() < 0.5:
            response = requests.get(RESOURCE_NODE_URL)
            logging.info(f"Read Request: {response.json()}")
        else:
            response = requests.post(RESOURCE_NODE_URL, json={"task": task})
            logging.info(f"Write Request: {response.json()}")

        lock_manager.release()

        request_end_time = time.time()
        response_times.append(request_end_time - request_start_time)

        time.sleep(random.uniform(0.1, 0.5))

    end_time = time.time()

    # Calculate total duration
    total_duration = end_time - start_time

    # Calculate throughput
    throughput = NUM_REQUESTS / total_duration

    # Calculate average response time
    avg_response_time = sum(response_times) / len(response_times)

    # Log analysis results
    logging.info(f"Total Duration: {total_duration} seconds")
    logging.info(f"Throughput: {throughput} requests/second")
    logging.info(f"Average Response Time: {avg_response_time} seconds")

    # Write analysis results to file
    with open("results.txt", "a") as file:
        file.write("Analysis Results:\n")
        file.write(f"Total Duration: {total_duration} seconds\n")
        file.write(f"Throughput: {throughput} requests/second\n")
        file.write(f"Average Response Time: {avg_response_time} seconds\n")

if __name__ == "__main__":
    simulate_read_write_requests()

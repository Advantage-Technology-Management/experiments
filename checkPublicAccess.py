import csv
import requests
import threading
from queue import Queue

# Configure the number of worker threads
NUM_WORKERS = 10

# Files
INPUT_FILE = './urltocheck.csv'
OUTPUT_FILE = 'results.log'

# Create a queue to hold the URLs
url_queue = Queue()

# Lock for logging to avoid race conditions
log_lock = threading.Lock()

def read_urls(file_path):
    """Reads URLs from a CSV file and adds them to the queue."""
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            url_queue.put(row[0])

def check_url():
    """Worker function to check the response code of a URL."""
    while not url_queue.empty():
        url = url_queue.get()
        try:
            response = requests.get(url)
            code = response.status_code
        except requests.RequestException as e:

            with log_lock:
                with open(OUTPUT_FILE, mode='a') as log_file:
                    log_file.write(f"{url},{e}\n")
        
        with log_lock:
            with open(OUTPUT_FILE, mode='a') as log_file:
                log_file.write(f"{url},{code},{len(response.content)}\n")
        
        url_queue.task_done()

def main():
    # Read URLs from the input file
    read_urls(INPUT_FILE)
    
    # Create worker threads
    threads = []
    for _ in range(NUM_WORKERS):
        thread = threading.Thread(target=check_url)
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

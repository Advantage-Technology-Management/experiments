import csv
import json
from urllib.parse import urlencode
import requests
import threading
from queue import Queue

# Configure the number of worker threads
NUM_WORKERS = 1

# Files
INPUT_FILE = './submitAEMworkflow.csv'
OUTPUT_FILE = 'submitAEMworkflowresults.log'

USERNAME='admin'
PASSWORD='S%j7?v<H{S3nTWgD[zjV0c*y'

HOST_URL = 'https://author-loblaw-stage.adobecqms.net/etc/workflow/instances'





HEADERS = {
    
    'Content-Type': 'application/json',
    'User-Agent': 'curl',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'author-loblaw-stage.adobecqms.net'
}


form_data = {

    'payloadType': 'JCR_PATH',
    'workflowTitle': 'LOBLAW MANUAL PROCESS PRODUCT',
    'startComment': 'ppw',
    'model': '/var/workflow/models/loblaw-manual-process-product'
    
}


# Create a queue to hold the URLs
request_queue = Queue()

# Lock for logging to avoid race conditions
log_lock = threading.Lock()

def read_urls(file_path):
    """Reads URLs from a CSV file and adds them to the queue."""
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            request_queue.put(row[0])

def check_url():
    """Worker function to check the response code of a URL."""
    while not request_queue.empty():
        form_data['payload'] = request_queue.get()
        #urlencoded_form_data = urlencode(form_data)


        try:
            print(f"HEADERS {HEADERS}\n")
            print(f"DATA {form_data}")
            
            response = requests.post(HOST_URL, data=form_data, auth=(USERNAME, PASSWORD), verify=False)
            code = response.status_code
            print(f"Response {response}{code}{response.reason}")
        except requests.RequestException as e:
            print(f"Exception encountered {e}")
            with log_lock:
                with open(OUTPUT_FILE, mode='a') as log_file:
                    log_file.write(f"{form_data},{e}\n")
        
        #with log_lock:
            #with open(OUTPUT_FILE, mode='a') as log_file:
                #log_file.write(f"{form_data},{code},{len(response.content)}\n")
        
        request_queue.task_done()

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

import requests
import csv
import threading

# Global lock for file writing
file_lock = threading.Lock()

# Static username and password
USERNAME="admin"
PASSWORD="S%j7?v<H{S3nTWgD[zjV0c*y"

PROTOCOL = 'https://'
HOST = 'author-loblaw-stage.adobecqms.net'
SERVICE_PATH = '/api/assets/loblaw-companies-limited/product-staging/manual/greg-test/gregtestfolder2/'
HEADERS= {'Host':'author-loblaw-stage.adobecqms.net'}

# Function to upload files to the endpoint
def upload_file(url, log_file):
    try:
        # Fetch the file from the URL
        response = requests.get(url, stream=True)
        
        # Check if the GET request was successful
        if response.status_code == 200:
            
            print("GET headers=")
            print(response.headers)
            # Retrieve the Content-Disposition header from the GET response
            content_disposition = response.headers.get('Content-Disposition', '')
            content_disposition_parts = content_disposition.split("=")
            postFilename = content_disposition_parts[1].strip('"').strip()
            print("Filename="+postFilename)
            # Set up the headers for the POST request, including Content-Type from Content-Disposition
            postHeaders = {
                'Content-Type': response.headers.get('Content-Type', ''),
                'Content-Disposition': content_disposition
            }
            postHeaders.update(HEADERS)
            print("Post Headers=")
            print(postHeaders)
            
            
            # Make the POST request with Basic Authentication and streamed content
            post_url = f"{PROTOCOL}{HOST}{SERVICE_PATH}{postFilename}"
            print("posturl="+post_url)
            post_response = requests.post(post_url, headers=postHeaders, data=response.iter_content(chunk_size=1024), auth=(USERNAME, PASSWORD))
            
            # Check if the POST request was successful
            if post_response.status_code == 201:
                log_message = f"File from {url} uploaded successfully.\n"
            else:
                log_message = f"Failed to upload file from {url}. Status code: {post_response.status_code}\n"
        else:
            log_message = f"Failed to fetch file from {url}. Status code: {response.status_code}\n"
    except Exception as e:
        log_message = f"An error occurred while processing file from {url}: {str(e)}\n"

    # Write log to file
    with file_lock:
        with open(log_file, 'a') as f:
            f.write(log_message)

# Function to handle file uploads in threads
def handle_uploads(urls, log_file):
    threads = []
    for url in urls:
        thread = threading.Thread(target=upload_file, args=(url[0], log_file))  # url[0] is the URL in the first column
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Read URLs from CSV file
def read_urls_from_csv(csv_file):
    urls = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            urls.append(row)
    return urls

# Main function
def main():
    # Number of threads
    num_threads = 5  # Change as needed

    # CSV file containing URLs
    csv_file = 'JFURLs.csv'  # Replace with your CSV file path

    # Log file
    log_file = 'upload_log.txt'

    # Read URLs from CSV file
    urls = read_urls_from_csv(csv_file)

    # Divide URLs into chunks based on number of threads
    chunk_size = len(urls) // num_threads
    url_chunks = [urls[i:i+chunk_size] for i in range(0, len(urls), chunk_size)]

    # Create and start threads
    threads = []
    for url_chunk in url_chunks:
        thread = threading.Thread(target=handle_uploads, args=(url_chunk, log_file))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

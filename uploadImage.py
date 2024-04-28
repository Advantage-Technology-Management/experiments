import json
import multiprocessing
from multiprocessing import Pool, TimeoutError

import requests
USERNAME='admin'
PASSWORD="S%j7?v<H{S3nTWgD[zjV0c*y"

CMD={'cmd',"activate"} 
PUBLISHURL='https://author-loblaw-prod.adobecqms.net/bin/replicate.json'
WORKFLOWURL='https://author-loblaw-prod.adobecqms.net/etc/workflow/instances'

def process_line(line):
    publicRequest = requests.get('https://dis-prod.assetful.loblaw.ca/'+line.split(",")[0]+'/_jcr_content/renditions/cq5dam.thumbnail.4096.4096.jpeg?imWidth=32')
    #print(publicRequest.elapsed.total_seconds())
    #print(publicRequest)
    if publicRequest.status_code != 200:        
        #print('https://dis-stage.assetful.loblaw.ca/content/product/'+line.split(",")[0]+'/_jcr_content/renditions/cq5dam.thumbnail.4096.4096.jpeg?imWidth=32')
        print('https://author-loblaw-prod.adobecqms.net/assetdetails.html'+line.split(",")[1].rstrip('\n'))
        #workflowPayload={'payload': line.split(",")[1].rstrip('\n'), 'payloadType' : 'JCR_PATH', 'workflowTitle' : 'LOBLAW DAM UPDATE ASSET', 'startComment' : 'Script triggered fix', 'model' : '/var/workflow/models/dam/loblawinc_dam_update_asset'}
        #w = requests.post(url=WORKFLOWURL,params=workflowPayload,auth=(USERNAME,PASSWORD))
        #print("Workflow",w.elapsed.total_seconds())
        #print('Workflow',w)

        #publishPayload={'path': line.split(",")[1].rstrip('\n'),'cmd': 'activate'}
        #print(payload)
        #p = requests.post(url=PUBLISHURL,params=publishPayload,auth=(USERNAME,PASSWORD))
        #print('Publish ',p)

if __name__ == "__main__":
    #outputfile = open('404URLS.txt','w')
    pool = Pool(2)
    with open('product_assets_to_be_activated_prod.csv',encoding='utf-8') as source_file:
        # chunk the work into batches of 4 lines at a time
        results = pool.map(process_line, source_file, 2)
        

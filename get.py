
import multiprocessing as mp
import requests
from functools import partial
from itertools import repeat


USER_NAME="admin"
PASSWORD="S%j7?v<H{S3nTWgD[zjV0c*y"
ENV='prod'

ACTIVATEURL='https://author-loblaw-'+ENV+'stage.adobecqms.net/bin/replicate.json'
WORKFLOWURL='https://author-loblaw-'+ENV+'.adobecqms.net/etc/workflow/instances'
PUBLISHERURL='https://dis-'+ENV+'.assetful.loblaw.ca'
RENDITION='/_jcr_content/renditions/cq5dam.web.4096.4096.jpeg'

def process_line(line, q):
    getRequest=PUBLISHERURL+line.rstrip()+RENDITION
    r = requests.get(getRequest+'?width=32')
    if r.status_code == 200:
        #print("Good",PUBLISHERURL+line.split(",")[0]+RENDITION)
        #print("Put good", getRequest)
        q.put(["Good",getRequest])
    
    else:
        #publishPayload={'path': line.split(",")[1].rstrip('\n'),'cmd': 'activate'}
        #print(publishPayload)
        #p = requests.post(url=ACTIVATEURL,params=publishPayload,auth=(USER_NAME,PASSWORD))
        #print(p.status_code)
        #print("Put bad",line.rstrip())
        q.put(["Bad",getRequest])
    return r
    
            
def outputFileQlistener(q):
    
    badfile = open('getFailure.txt', 'w')
    goodfile = open('getSuccess.txt', 'w')

    
    while 1:
        m = q.get()
        if m == 'kill':
            break
        if m[0] == "Good":
            goodfile.write(str(m[1]+"\n"))
            goodfile.flush
        else:
            badfile.write(str(m[1]) + '\n')
            badfile.flush()

if __name__ == "__main__":
    queueManager = mp.Manager()
    outputFileQ = queueManager.Queue()
        
    pool = mp.Pool(4)
    outputWatcher = pool.apply_async(outputFileQlistener, (outputFileQ,))
    
    with open('product_assets_to_be_activated_prod.csv') as source_file:
        pool.starmap(process_line, zip(source_file, repeat(outputFileQ)),10)
        
    outputFileQ.put('kill')
    pool.close()
    pool.join()    
    

        
 

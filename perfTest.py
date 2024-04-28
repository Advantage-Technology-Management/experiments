
import multiprocessing as mp
import requests
from functools import partial
from itertools import repeat
import time, datetime


#USER_NAME="admin"
#PASSWORD="S%j7?v<H{S3nTWgD[zjV0c*y"


def process_line(line, q):
    URL = line.rstrip()
    r = requests.get(URL)
    #print(r.status_code)
    #print(r.elapsed.total_seconds())
    if r.status_code == 200:
        #print("Good",PUBLISHERURL+line.split(",")[0]+RENDITION)
        #print("Put good", getRequest)
        #q.put(["Good",URL + ', ' + r.elapsed())
        message = URL + ", " + str(r.elapsed.total_seconds())
        #print(message)
        q.put(["Good", message])
    else:
        #q.put(["Bad",URL + ', ' + r.status_code])
        message = URL + ", " + str(r.status_code)
        #print(message)
        q.put(["Bad", message])
              #+ URL + ', ' + r.status_code])
    return r
    
            
def outputFileQlistener(q):
    
    badfile = open('badoutputfile', 'w')
    goodfile = open('goodoutputfile', 'w')

    
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
        
    pool = mp.Pool(50)
    outputWatcher = pool.apply_async(outputFileQlistener, (outputFileQ,))
    
    with open('StageDirectPublic650.csv') as source_file:
        pool.starmap(process_line, zip(source_file, repeat(outputFileQ)),100)
        
    outputFileQ.put('kill')
    pool.close()
    pool.join()    
    

        
 

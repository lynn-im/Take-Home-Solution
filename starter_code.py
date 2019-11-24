import mock_db
import uuid
from worker import worker_main
from threading import Thread
import os
import time
import sys
import logging

debug = False

def lock_is_free(worker_hash, db):
    """
        CHANGE ME, POSSIBLY MY ARGS
        Return whether the lock is free
    """
    
    # DB Locked is an arbitrary value to be assigned to the key "_id" and written to the DB
    # The presence of the key in the DB means the "worker_main" process is locked for use by a single thread. 
    key_val_pair = { "_id": "********DB is Locked**********" }
 
    #DBlocked indicates if the DB record used to indicate a Lock is written or not. 
    DBlocked = True
    while DBlocked:    #keep trying until all threads are complete
        try:
            #try to lock the DB by writing the record used to indicate a Lock is written or not
            db.insert_one(key_val_pair)  
            print ("Lock DB and start worker_main for thread: ", worker_hash)
            return key_val_pair

        # Unable to get the create the lock - means a DuplicateKeyError exception will be raised AND means we must wait and try again later  
        except Exception as e: 
            if debug: print(str(e), "exception")
            time.sleep(2) #DB is locked wait for it to be free and try again
    
    return key_val_pair


def attempt_run_worker(worker_hash, give_up_after, db, retry_interval):
    """
        CHANGE MY IMPLEMENTATION, BUT NOT FUNCTION SIGNATURE

        Run the worker from worker.py by calling worker_main

        Args:
            worker_hash: a random string we will use as an id for the running worker
            give_up_after: if the worker has not run after this many seconds, give up
            db: an instance of MockDB
            retry_interval: continually poll the locking system after this many seconds
                            until the lock is free, unless we have been trying for more
                            than give_up_after seconds
    """
    # Pass this worker over to set the lock needed to write to output.txt and
    # return the key/value needed to release the lock after the write to output.txt
    key_val_pair = lock_is_free(worker_hash, db)
    try:
        worker_main(worker_hash, db)  #write the message to output.txt
    except Exception as e:
        print(str(e), "exception")   #worker_main will crash sometimes, so this can log the crash 
    
    #release the lock 
    db.delete_one(key_val_pair)
    print ("Release DB")

       
if __name__ == "__main__":
    """
        DO NOT MODIFY

        Main function that runs the worker five times, each on a new thread
        We have provided hard-coded values for how often the worker should retry
        grabbing lock and when it should give up. Use these as you see fit, but
        you should not need to change them
    """

    db = mock_db.DB()
    threads = []
    for _ in range(25):       
        t = Thread(target=attempt_run_worker, args=(uuid.uuid1(), 2000, db, 0.1))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
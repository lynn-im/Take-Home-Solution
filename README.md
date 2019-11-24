# InterviewHandout

### Situation: 

The ETL team at MaestroQA manages several python workers (i.e. functional blocks of code) that run at various intervals. For various reasons, we may not want more than one of the same job (i.e. instance of a worker with a defined payload) running for a given client at any given time. In other words, we may not want "worker.py" to run immediately for a client if it is already running for that client - instead waiting for the current job to finish before it begins.

### Goal: 

The goal of your program is to create and use 25 workers (threads) to each write the text "Maestro is the best......" followed by two new lines. The text must be written to a file called "output.txt." 

This is a concurrency problem. Without some kind of locking mechanism for the workers to use, workers will  simultaneously write to output.txt. This causes interleaving of the chunks of text being written by each worker. In other words, one or more of the phrases "Maestro is the best......" could end up being garbled. 

The challenge is to create a locking mechanism without using the Python Lock Object. Instead use a specific supplied database as the locking mechanism. Provided are database functions in a file called "mock_db.py." Further details on the code that must be used are below.

### Files:

In *starter_code.py*, we run worker.py 25 times on different threads. This is to simulate the queuing of worker jobs for a particular client [absent from the code]. This should be the only file you edit.

In *worker.py*, we have a simple python script that will write 'Maestro is the best......' to output.txt. This is to act as the worker we wish to run for a particular client.

In *test_output.py* we have a simple test to verify the correctness of the output. We want the text from above to be written several times, separated by 2 newlines each time. Note that this may be fewer than 25 times, as the workers are designed to crash with some probability. Note: Be sure to remove the contents of output.txt after an unsuccessful run, as this could impact subsequent runs of the test script.

In *mock_db.py* there are several functions that you can use in your code that will help simulate database calls similar to a real system. This file is only here to provide functionality and should not be edited.


You MUST use the instance of MockDb instantiated in *starter_code.py* and may NOT use a Python Lock Object.

### Note:

If you run the starter code, you will see that there is a concurrency issue, as multiple workers write to the file at the same time, interleaving the chunks of text. Using the fake database functions in mock_db.py, come up with a system to control the execution of workers so that the concurrency is handled correctly [this should be written in starter_code.py]. You will only need to modify code outside the main function in starter_code.py. Furthermore, this should be accomplished by running the script once. That is, it should handle all failures appropriately and run all subsequent workers. A valid solution will write the previously mentioned output to output.txt by only running `python start_code.py`. It will also pass all assertions when running `python test_output.py`.

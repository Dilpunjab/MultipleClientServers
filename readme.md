## worker.py 
	python3 worker.py portnumber
	You should run worker file first.
	Here portnumber are the port where worker will run
	You can use and unused port number from 1 to 65535.

## coordinator.py
	python3 coordinator.py portnumber localhost:port localhost:port
	After running worker file you should run coordinator file.
	here portnumber id port where coordinator will run 
	localhosts are the workers

## test_cli.py
	python3 test_cli.py portnumber(coordinator)
	then you can run your test file with giving port number of coordinator as parameter		


## test.py
	this file is made for 2PC specifications. and sends specific commands to coordinator and runs unit test for workers. but this file is incomplete

### Problems
	I am having problems in handling multiple workers and test file	
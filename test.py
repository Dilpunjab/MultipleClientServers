import cmd
import sys
import re
import json
import socket


HEADER_L = 2048
port= int(sys.argv[1])
host = '127.0.0.1'
try:
	print(f"Starting server on port:{port} ")
	print("type set to set value to key or get to fetch value of key and get-db for whole database")

except Exception as e:
	print(e)
	sys.exit(1)	

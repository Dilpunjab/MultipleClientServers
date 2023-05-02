import cmd
import sys
import json
import socket

# worker starting on port -----
# request from('128.0.1',54594)
# timeout
database = {
    "hey" : "thing"
}

get_val = " "
worker_port = int(sys.argv[1])
worker_host = '127.0.0.1'
print(f"Working starting on port: {worker_port}")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # blocking, but default
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # overall timeout
    # s.settimeout(5)
s.bind((worker_host, worker_port))
s.listen(1)
clientsocket, address = s.accept()
print(f"request from {address}")
print("timeout set for 60")
while True:
        try:
            tmp =  clientsocket.recv(2048)
            clientsocket.sendall(tmp)
            newtmp = json.loads(tmp)
            # timeout set to 60
            if newtmp : 
                print("Got Query for " + newtmp["key"])

                if newtmp["type"] == "SET":
                    if newtmp is not None:
                        content ={"type": "QUERY-REPLY", "key": newtmp['key'], "answer": True }
                    else:
                        content ={"type": "QUERY-REPLY", "key": newtmp['key'], "answer": False }
                    database[newtmp['key']] = newtmp['value']
                    if database.get(newtmp['key']) is not None: 
                        comit ={"type": "COMMIT-REPLY", "key": newtmp['key'], "value": newtmp['value'], "answer": True } 
                        print(f"Got commit for {newtmp['key']}")
                    else:
                        comit ={"type": "COMMIT-REPLY", "key": newtmp['key'], "value": newtmp['value'], "answer": False }
                        print("not able to updated database")
                
                elif newtmp["type"] == "GET":
                    print("im in")
                    content ={"type": "QUERY-REPLY", "key": newtmp["key"] }
                    if newtmp['key'] in database:
                        comit ={"type": "COMMIT-REPLY", "key": newtmp["key"], "value": database[newtmp["key"]]}
                    else:
                        comit ={"type": "COMMIT-REPLY", "key": newtmp["key"], "value": null}
                        print("not in database")

                elif newtmp["type"] == "GET-DB":  
                    content = {"type": "QUERY-REPLY"} 
                    get_val = database  
                    comit ={"the":"database" , database["key"]:database["value"]}
                clientsocket.sendall(json.dumps(content).encode()) 
                clientsocket.sendall(json.dumps(comit).encode())
                print(database)
        
        except IOError as e:     
            print(e)
clientsocket.close()
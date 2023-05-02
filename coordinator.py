import socket
import sys
import select
import json


HEADER_L = 2048
coor_port= int(sys.argv[1])
coor_host = '127.0.0.1'
print(f"Starting server on port:{coor_port} ")


def add_port(temp):
    parts = temp.split(':')
    return (parts[0] , int(parts[1]))
# it = add(sys.argv[3])    
# def add_worker(worker_host,worker_port):
#     worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     worker_socket.connect((worker_host,int(worker_port)))
#     worker_dict[worker_socket] = worker_port
#     inputs.append(worker_socket)

worker_dict = { }    


work_arr = list(map(add_port,sys.argv[2:]))
print(work_arr)

worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
worker_socket.connect((coor_host,5005))   


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind((coor_host,coor_port))
    server_socket.listen(1)
    # clientsocket, address = client_socket.accept()
    # print("Adding client "+ address )

    client_socket_list = [server_socket]
    clients = {}

    def recieve_msg(client_socket):
        try:
            message = client_socket.recv(HEADER_L)
            
            if not len(message):
                return False
            print(message)    
            data =json.loads(message)
            if (data['type'] == 'SET'):
                print(f"New Request: Request: {data['key']}:{data['value']}")
                print(data)
            elif (data['type'] == 'GET'):  
                print(f"New Request: Request: {data['key']}")  
            return message
            # clients.sendall(b"message recieved")
        except Exception as e :
            print(e)
            return False


    def worker_premission():
        try:
            worker_socket.sendall(b'can you work or not')
            worker_data = worker_socket.recv(2048)
            if worker_data == True:
                # worker_socket.
                return True
            else:
                worker_socket.close()   

        except :
            return False  

    inputs = [server_socket,worker_socket]
    outputs = []
    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for source in readable:
            try:
                if source is server_socket:
                    clientsocket, address = server_socket.accept()
                    inputs.append(clientsocket)
                    print(f"Adding client {address}")
                    

                if source is worker_socket:       
                    try:    
                        message = worker_socket.recv(HEADER_L)
                        if not len(message):
                            print("no message recieved from worker")
                        print(message)
                        # print(data)

                        query_msg = worker_socket.recv(HEADER_L)
                        print(query_msg)
                        commit_msg = worker_socket.recv(HEADER_L)
                        print(commit_msg)
                        
                        clientsocket.sendall(commit_msg)
                         
                        # clientsocket.sendall(b"message recieved")
                    except :
                        print("can't recieve message from worker")
                        clientsocket.close()
                        worker_socket.close()

                if source is clientsocket:
                    temp =  recieve_msg(clientsocket)
                    print(temp)
                    if temp :
                        worker_socket.send(temp) 
                    else :
                        print("can't send message to workers") 
            except Exception as e:
                print(e) 
                clientsocket.close()
                worker_socket.close()
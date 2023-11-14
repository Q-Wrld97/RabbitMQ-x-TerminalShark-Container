import socket
import bson
import threading

def handle_client(conn):
    data = conn.recv(4096)
    obj = bson.loads(data)
    print(obj)
    
    conn.close()

def parse_bson_obj(obj):
    pass

def send_bson_obj():
    pass

def receive_bson_obj():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12345))
        s.listen()

        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
    

if __name__ == '__main__':
    receive_bson_obj()

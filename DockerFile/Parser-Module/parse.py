import socket
import bson
import threading
import pika
from pika.exchange_type import ExchangeType

def handle_client(conn):
    data = conn.recv(4096)
    obj = bson.loads(data)
    print(obj)
    parse_bson_obj(obj)
    conn.close()

def parse_bson_obj(obj):
    data_types = {
        'Documents': '.Document.',
        'Images': '.Image.',
        'Audio': '.Audio.',
        'Video': '.Video.'
    }

    for data_type, routing_key in data_types.items():
        if obj[data_type]:
            for item in obj[data_type]:
                publish_to_rabbitmq(routing_key, item)
        else:
            print(f"No {data_type.lower()} to send")

def publish_to_rabbitmq(routing_key,message):
    # Establish a connection to RabbitMQ server
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel
    channel = connection.channel()
  
    message= bson.dumps(message)
    
    # Publish a message to the specified routing key
    channel.basic_publish(
        exchange="Topic",
        routing_key=routing_key,
        body=message
    )

    print(f'Message "{message}" sent on routing key "{routing_key}"')

    # Close the connection
    connection.close()
    #sent over the bus

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

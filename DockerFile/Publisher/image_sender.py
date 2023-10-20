import pika
from pika.exchange_type import ExchangeType
from pika.spec import BasicProperties
import os
import bson

def publish_message(routing_key, message):
    # Establish a connection to RabbitMQ server
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel
    channel = connection.channel()

    # Declare an exchange of type 'topic' (if it doesn't exist already)
    exchange_name = 'Preprocess'
    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.topic, durable=True)
    
   
    
    # Publish a message to the specified routing key
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=message
    )

    print(f'Message "{message}" sent on routing key "{routing_key}"')

    # Close the connection
    connection.close()


# Path to the image file
image_path = 'DockerEnv/DockerFile/Publisher/x.png' 

# Print debugging information
print(f"Current working directory: {os.getcwd()}")
print(f"Image path: {image_path}")
print(f"File exists: {os.path.exists(image_path)}")  
#read in a.png
with open(image_path, 'rb') as image_file:
    data = image_file.read()

#message ={
#    'image':data,
#    'name':'x.png'
#}
#message = bson.dumps(message)

message = data

# Publish messages
publish_message('Preprocess.Image', message)




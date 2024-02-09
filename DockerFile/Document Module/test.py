import pika
import bson


# Function to publish messages to RabbitMQ
def publish_to_rabbitmq(routing_key, message):
    # Establish a connection to the RabbitMQ server
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel for communication with RabbitMQ
    channel = connection.channel()
  
    # Serialize the message to BSON
    message = bson.dumps(message)
    
    # Publish the message to the specified routing key
    channel.basic_publish(
        exchange="Topic",
        routing_key=routing_key,
        body=message
    )

    print(f'Message "{message}" sent on routing key "{routing_key}"')

    # Close the connection to RabbitMQ
    connection.close()
    

body = {
    "ID": "ObjectID",  
    "DocumentId": "ObjectID",
    "DocumentType": "String",
    "FileName": "String",
    "Payload": "Binary"
}

# take binary data from file
with open('Project_4.pdf', 'rb') as f:
    body['Payload'] = f.read()
    f.close()


publish_to_rabbitmq('Document', body)
import pika
from pika.exchange_type import ExchangeType

# Establish a connection to RabbitMQ server
connection_parameters = pika.ConnectionParameters('rabbitmq_tshark')
connection = pika.BlockingConnection(connection_parameters)

# Create a channel
channel = connection.channel()

routing_keys = {
    'Error': [
        'Error.Process',
        'Error.Store',
        'Error.Preprocess',
        'Error.*'
    ],
    'Store': [
        'Store.Image',
        'Store.Image.Status',
        'Store.Document',
        'Store.Document.Status',
        'Store.*'
    ],
    'Process': [
        'Process.Document',
        'Process.Document.Status',
        'Process.Image',
        'Process.Image.Status',
        'Process.*'
    ],
    'Preprocess': [
        'Preprocess',
        'Preprocess.Document',
        'Preprocess.Document.ACK',
        'Preprocess.Image',
        'Preprocess.Image.ACK',
        'Preprocess.*'
    ]
}

# Declare exchanges, queues, and bind them with the specified routing keys
for exchange_name, keys in routing_keys.items():
    # Declare an exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.topic, durable=True)
    
    for routing_key in keys:
        # Declare a queue (queue names are generated based on the routing key)
        queue_name = routing_key  # Replace '.' with '_' to form valid queue names
        channel.queue_declare(queue=queue_name, durable=True)

        # Bind the queue to the exchange with the routing key
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

# Close the connection
connection.close()

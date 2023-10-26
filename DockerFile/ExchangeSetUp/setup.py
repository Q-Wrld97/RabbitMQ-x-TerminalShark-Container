import pika
from pika.exchange_type import ExchangeType

# Establish a connection to RabbitMQ server
connection_parameters = pika.ConnectionParameters('rabbitmq_tshark')
connection = pika.BlockingConnection(connection_parameters)

# Create a channel
channel = connection.channel()

routing_keys = [
    "#.Document.#",
    "#.Store.#",
    "#.Image.#",
    "Error.*",
]

channel.exchange_declare(exchange='Topic', exchange_type=ExchangeType.topic, durable=True)

# Declare queues
for key in routing_keys:
    channel.queue_declare(queue=key, durable=True)
    #bind queues to exchange
    channel.queue_bind(exchange='Topic', queue=key, routing_key=key)


# Close the connection
connection.close()

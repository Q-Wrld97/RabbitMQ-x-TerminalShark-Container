import pika
from pika.exchange_type import ExchangeType
import bson

def consumer_connection(routing_key):
    # Establish a connection to RabbitMQ server
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel
    channel = connection.channel()

    # Declare an exchange of type 'topic' (if it doesn't exist already)
    exchange_name = 'Preprocess'
    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.topic, durable=True)

    # Declare a queue (queue names are generated based on the routing key)
    queue_name = routing_key
    channel.queue_declare(queue=queue_name, durable=True)

    # Bind the queue to the exchange with the routing key
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    #call back function
    def on_message_received(ch, method, properties, body):
        #body=bson.loads(body)
        #save the image
        with open('DockerEnv/DockerFile/Consumer/x.png', 'wb') as image_file:
            image_file.write(body)
            
        print(f"""
                {routing_key} - received new message: {body}
                routing key: {method.routing_key}
                properties: {properties.delivery_mode}
                channel: {ch}""")
    
    # Consume messages from the queue
    a=channel.basic_consume(queue=queue_name, auto_ack=True,
        on_message_callback=on_message_received)
    

    
    
    print('Preprocess Starting Consuming')
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.close()
        connection.close()


consumer_connection('Preprocess.Image')
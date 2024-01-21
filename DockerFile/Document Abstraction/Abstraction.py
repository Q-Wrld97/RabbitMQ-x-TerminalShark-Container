import requests
import bson
import pika
import threading


url="http://localhost:5000"

def consume_document():
    # Establish a connection to RabbitMQ server
    connection_parameters = pika.ConnectionParameters('rabbitmq_tshark')
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel
    channel = connection.channel()

    # Declare a queue (queue names are generated based on the routing key)
    queue_name = 'Document'

    # Consume messages from the queue
    channel.basic_consume(queue=queue_name, auto_ack=True,
        on_message_callback=on_message_received)
    
    print('Starting Consuming')
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.close()
        connection.close()

def on_message_received(ch, method, properties, body):
    body=bson.loads(body)
    document = body['Payload']
    # Create a new thread for each send_job call
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, send_job, document, body)

def send_job(document, body):
    headers = {
        'Content-Type': 'application/bson'
    }
    response = requests.post(f"{url}/send_job", data=document, headers=headers)
    # Check if the response's content type is BSON
    if response.headers.get('Content-Type') == 'application/bson':
        # Decode the BSON data
        data = response.content
        print(data)
    else:
        print("Response is not in BSON format.")


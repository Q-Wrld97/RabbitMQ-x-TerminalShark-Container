import requests
import bson
import pika
import asyncio

url="http://localhost:5000"

def consume_document():
    # Establish a connection to RabbitMQ server
    # 'rabbitmq_tshark' is the host of the RabbitMQ server
    connection_parameters = pika.ConnectionParameters('rabbitmq_tshark')
    
    # Create a blocking connection with the RabbitMQ server
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel on the connection
    channel = connection.channel()

    # Declare a queue to consume from, in this case, the queue is named 'Document'
    queue_name = 'Document'

    # Start consuming messages from the declared queue
    # on_message_received is the callback function that will be called when a message is received
    channel.basic_consume(queue=queue_name, auto_ack=True,
        on_message_callback=on_message_received)
    
    print('Starting Consuming')
    
    # Start the consuming process
    # This will block the current thread and loop over incoming messages
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        # If a keyboard interrupt is received, stop consuming and close the connection
        channel.close()
        connection.close()

def on_message_received(ch, method, properties, body):
    # Load the BSON data from the body
    body=bson.loads(body)
    
    # Extract the 'Payload' from the body
    document = body['Payload']
    
    # Get the current event loop
    loop = asyncio.get_event_loop()
    
    # Run the send_job function in a separate thread, passing document and body as arguments
    # This is done to prevent blocking the event loop if send_job takes a long time to run
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


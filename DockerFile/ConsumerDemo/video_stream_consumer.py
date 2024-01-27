import asyncio
import signal
import pika
from rstream import (
    AMQPMessage,
    Consumer,
    MessageContext,
    amqp_decoder
)

STREAM = "Video"

def delete_queue(queue_name):
    # Establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Delete the queue
    channel.queue_delete(queue=queue_name)

    # Close the connection
    connection.close()

async def consume():
    consumer = Consumer(
        host="localhost",
        port=5552,
        vhost="/",
        username="guest",
        password="guest",
    )

    async def on_message(msg: AMQPMessage, message_context: MessageContext):
        stream = message_context.consumer.get_stream(message_context.subscriber_name)
        offset = message_context.offset

        # Write the video data to a file
        with open('received_video.mp4', 'wb') as file:
            file.write(msg)
            consumer.stop()
            delete_queue(STREAM)

    await consumer.start()
    await consumer.subscribe(stream=STREAM, callback=on_message)
    await consumer.run()

    # Delete the stream after all messages are consumed
   

asyncio.run(consume())
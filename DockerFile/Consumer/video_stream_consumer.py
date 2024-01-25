import asyncio
import signal

from rstream import (
    AMQPMessage,
    Consumer,
    MessageContext,
    amqp_decoder,
)

STREAM = "my-test-stream"

async def consume():
    consumer = Consumer(
        host="127.0.0.1",
        vhost="/",
        username="guest",
        password="guest",
    )

    async def on_message(msg: AMQPMessage, message_context: MessageContext):
        stream = message_context.consumer.get_stream(message_context.subscriber_name)
        offset = message_context.offset
        print("Got message: {} from stream {}, offset {}".format(msg, stream, offset))

    try:
        await consumer.start()
        await consumer.subscribe(stream=STREAM, callback=on_message)
        await consumer.run()
    except KeyboardInterrupt:
        await consumer.close()

asyncio.run(consume())
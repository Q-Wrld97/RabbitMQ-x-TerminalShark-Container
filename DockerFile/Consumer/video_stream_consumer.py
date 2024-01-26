import asyncio
from rstream import AMQPMessage, Consumer, MessageContext

STREAM = "my-test-stream"

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
        await message_context.
        print("Got message: {} from stream {}, offset {}".format(msg, stream, offset))

    await consumer.start()
    await consumer.subscribe(stream=STREAM, callback=on_message)
    
    try:
        await consumer.run()
    except KeyboardInterrupt:
        await consumer.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        await consumer.close()

asyncio.run(consume())
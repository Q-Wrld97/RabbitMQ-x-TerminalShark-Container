import asyncio
import time

from rstream import AMQPMessage, Producer

STREAM = "Video"

async def publish():
    async with Producer("localhost", username="guest", password="guest") as producer:
        # create a stream if it doesn't already exist
        await producer.create_stream(STREAM, exists_ok=True)

        # Read the video file in binary mode
        with open('my_video.mp4', 'rb') as file:
            video_data = file.read()

        # Send the video data as a message
        await producer.send(stream=STREAM, message=video_data)

        print(f"Sent video file as a message")

asyncio.run(publish())



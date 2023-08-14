import asyncio
import json
import os
import random

import aio_pika

input_data = {
    "correlation_id": 13242421424214,
    "phones": [str(random.randint(0, 200)) for _ in range(10)]
}


async def publish_messages(message_body) -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/",
    )
    message_body = json.dumps(message_body).encode('utf-8')

    async with connection:
        routing_key = os.getenv("QUEUE_NAME")

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key=routing_key,
        )


async def main():
    tasks = [publish_messages(input_data) for _ in range(10)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

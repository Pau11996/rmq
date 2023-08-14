import json
import os
from datetime import datetime

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.core.db import get_postgres_session

import aio_pika

from app.phones.phone_schema import ResponseSchema
from app.phones.utils import generate_report

router = APIRouter()


@router.get('/consume')
async def consume_report_data(session: Session = Depends(get_postgres_session)):

    start_date = datetime.now()
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/",
    )
    queue_name = os.getenv('QUEUE_NAME')

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                results = []
                report_queue = os.getenv('REPORT_QUEUE')
                async with message.process():
                    input_data = json.loads(message.body)

                    for phone in input_data["phones"]:
                        report = await generate_report(session, phone)
                        results.append(report.model_dump())

                    if queue.name in message.body.decode():
                        break

                total_duration = datetime.now() - start_date
                response = ResponseSchema(
                    correlation_id=input_data["correlation_id"],
                    data=results,
                    total_duration=str(total_duration)
                )

                message_body = json.dumps(response.model_dump()).encode('utf-8')
                await channel.default_exchange.publish(
                    aio_pika.Message(body=message_body),
                    routing_key=report_queue,
                )


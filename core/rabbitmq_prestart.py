import logging
from uuid import uuid4

import pika
import pika.exceptions
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from core.configs import settings
from core.logger import logger

@retry(
    stop=stop_after_attempt(settings.RABBITMQ_CONNECTION_MAX_TRIES),
    wait=wait_fixed(settings.RABBITMQ_WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_rabbitmq_connection() -> bool:
    """
    Function to check RabbitMQ Connection
    :return: boolean whether the connection is successful or not
    """
    is_rabbitmq_need_auth = settings.RABBITMQ_USE_CREDENTIALS
    rabbitmq_host = settings.RABBITMQ_HOST
    rabbitmq_port = settings.RABBITMQ_PORT
    rabbitmq_username = settings.RABBITMQ_USERNAME
    rabbitmq_password = settings.RABBITMQ_PASSWORD

    response = False
    try:
        if is_rabbitmq_need_auth:
            logger.info(f"init_rabbitmq_connection: [ReqId: {str(uuid4())}] Connecting to RabbitMQ using Credentials.")
            rmq_credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                rabbitmq_host,
                rabbitmq_port,
                '/',
                rmq_credentials,
                heartbeat=60,
            ))
        else:
            logger.info(f"init_rabbitmq_connection: [ReqId: {str(uuid4())}] Connecting to RabbitMQ without using Credentials.")
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, heartbeat=60))
        channel = connection.channel()

        logger.info(f"init_rabbitmq_connection: [ReqId: {str(uuid4())}] RabbitMQ Connection is Online.")
        response = True
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"init_rabbitmq_connection: [ReqId: {str(uuid4())}] Error connecting to RabbitMQ: {e}", exc_info=True)

    return response

if __name__ == '__main__':
    init_rabbitmq_connection()

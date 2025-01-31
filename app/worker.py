import asyncio
import aio_pika
import logging
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_message(message: aio_pika.IncomingMessage):
    """
    Callback function to process incoming messages from the queue.
    """
    async with message.process():
        try:
            filename = message.body.decode()
            logger.info(f"Processing: {filename}")
            # Your compression logic here
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

async def main():
    """
    Main function to connect to RabbitMQ and start consuming messages.
    """
    retries = 5
    for i in range(retries):
        try:
            # Attempt to connect to RabbitMQ
            connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
            logger.info("Successfully connected to RabbitMQ")
            break
        except Exception as e:
            logger.error(f"Connection attempt {i + 1} failed: {e}")
            if i < retries - 1:
                await asyncio.sleep(5)  # Wait before retrying
    else:
        # If all retries fail, raise an exception
        raise Exception("Failed to connect to RabbitMQ after multiple attempts")

    try:
        async with connection:
            # Create a channel
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)  # Limit the number of unacknowledged messages

            # Declare a durable queue
            queue = await channel.declare_queue(
                settings.queue_name,
                durable=True
            )
            logger.info(f"Queue '{settings.queue_name}' declared")

            # Start consuming messages
            logger.info("Worker started. Waiting for messages...")
            await queue.consume(process_message)

            # Keep the event loop running
            await asyncio.Future()  # Run indefinitely
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
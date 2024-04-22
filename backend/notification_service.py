# Sends notification to the user
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os

load_dotenv()

consumer = KafkaConsumer(
    'Test',
    bootstrap_servers=os.getenv('KAFKA_SERVER_URL'),
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    sasl_plain_username=os.getenv('KAFKA_USERNAME'),
    sasl_plain_password=os.getenv('KAFKA_PASSWORD'),
    group_id='YOUR_CONSUMER_GROUP',
    auto_offset_reset='earliest'
)

try:
    for message in consumer:
        print(f"Received message: {message.value}")
        # Perform Notification Logic Here
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
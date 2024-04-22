from kafka import KafkaProducer
from dotenv import load_dotenv
import os
load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_SERVER_URL'),
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    sasl_plain_username=os.getenv('KAFKA_USERNAME'),
    sasl_plain_password=os.getenv('KAFKA_PASSWORD')
)

try:
    producer.send('Test', b'Hello from python')
    producer.flush()
    print("Message produced without Avro schema!")
except Exception as e:
    print(f"Error producing message: {e}")
finally:
    producer.close()
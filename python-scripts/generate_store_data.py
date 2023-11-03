import random
import json
import faker
from confluent_kafka import Producer
from decimal import Decimal

# Create a Faker instance
fake = faker.Faker()

# Kafka configuration
conf = {
    'bootstrap.servers': '[Broker_URL]',        # Add your Kafka broker(s) here
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': '[Cloud_API_Key]',          
    'sasl.password': '[Cloud_API_Secret]'           
}

# Function to generate mock store information
def produce_store_info(producer, num_stores):
    while True:
        store_info = []
        for _ in range(num_stores):
            store = {
                'SKU': fake.random_int(min=1000, max=9999),  # SKU
                'segment': fake.random_element(elements=('SegmentA', 'SegmentB', 'SegmentC')),  # Segment
                'variant': fake.random_element(elements=('Variant1', 'Variant2', 'Variant3')),  # Variant
                'latitude': float(fake.latitude()),  # Latitude
                'longitude': float(fake.longitude()),  # Longitude
                'country': "USA"
            }
            store_info.append(store)

        # Produce the store information to the Kafka topic
        
        for store in store_info:
            store_data_json = json.dumps(store)
            producer.produce("stores_products", value=store_data_json)

        # Wait for any outstanding messages to be delivered and delivery reports to be received
        producer.flush()

def main():
    p = Producer(conf)
    num_stores = 1  # Change this number to generate more or fewer stores
    produce_store_info(p, num_stores)
    print(f"Produced {num_stores} store events.")

if __name__ == "__main__":
    main()

import random
import json
import faker
from confluent_kafka import Producer
from decimal import Decimal

# Create a Faker instance
fake = faker.Faker()

# Kafka configuration
conf = {
    'bootstrap.servers': 'pkc-921jm.us-east-2.aws.confluent.cloud:9092',        # Add your Kafka broker(s) here
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'KHMDL6NACBUOJ2TA',            # Add your SASL username
    'sasl.password': 'dBpH4Ee9cM7PSwwsrueKVCnyt8R0bNxnvsvQkdbEfIg2LGiFeARsBBU0hP93wjYb'             # Add your SASL password
}

# Function to generate mock customer location data
def produce_location_info(producer, num_locations):
    while True:
        location_info = []
        for _ in range(num_locations):
            location = {
                'latitude': float(fake.latitude()),    # Latitude
                'longitude': float(fake.longitude()),  # Longitude
                'uid': fake.uuid4(),                # Generate a random UUID as uid
                'country': "USA"
            }
            location_info.append(location)

        # Produce the location information to the Kafka topic
        for location in location_info:
            location_data_json = json.dumps(location)
            producer.produce("customers-locations", value=location_data_json)

        # Wait for any outstanding messages to be delivered and delivery reports to be received
        producer.flush()

def main():
    p = Producer(conf)
    num_locations = 1  # Change this number to generate more or fewer location records
    produce_location_info(p, num_locations)
    print(f"Produced {num_locations} location events to customers.locations topic.")

if __name__ == "__main__":
    main()

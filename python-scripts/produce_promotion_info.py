import random
import json
import faker
from confluent_kafka import Producer

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

# Function to generate mock promotion data
def produce_promotion_info(producer, num_promotions):
    while True:
        promotion_info = []
        for _ in range(num_promotions):
            promotion = {
                'pid': fake.uuid4(),                      # Generate a random UUID as pid
                'SKU': fake.random_int(min=1000, max=9999),  # SKU
                'segment': fake.random_element(elements=('SegmentA', 'SegmentB', 'SegmentC'))  # Segment
            }
            promotion_info.append(promotion)

        # Produce the promotion information to the Kafka topic
        for promotion in promotion_info:
            promotion_data_json = json.dumps(promotion)
            producer.produce("products-promotions", value=promotion_data_json)

        # Wait for any outstanding messages to be delivered and delivery reports to be received
        producer.flush()

def main():
    p = Producer(conf)
    num_promotions = 1 # Change this number to generate more or fewer promotions
    produce_promotion_info(p, num_promotions)
    print(f"Produced {num_promotions} promotion events to products.promotions topic.")

if __name__ == "__main__":
    main()

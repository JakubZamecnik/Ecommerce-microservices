import pika
import json
import time
from config import settings

def process_order(ch, method, properties, body):
    data = json.loads(body)
    order_id = data.get("order_id")
    product = data.get("product_name")
    
    print(f" [📦] Přijata objednávka č. {order_id} na zboží: {product}")
    print(" [⚙️] Rezervuji zboží v databázi skladu...")
    time.sleep(2)  # Simulace práce
    print(f" [✅] Zboží pro objednávku {order_id} rezervováno!")
    
    # Potvrzení RabbitMQ, že zpráva byla zpracována
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_inventory_service():
    # Retry logika, kdyby RabbitMQ startovalo pomaleji
    for i in range(10):
        print(" [DEBUG] Inventory Service se pokouší nastartovat...", flush=True)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.rabbitmq_host))
            channel = connection.channel()
            channel.queue_declare(queue='order_created')

            channel.basic_consume(queue='order_created', on_message_callback=process_order)

            print(' [*] Inventory Service čeká na zprávy. Ukončíš pomocí CTRL+C')
            channel.start_consuming()
            break
        except Exception:
            print(f" [!] Čekám na RabbitMQ... ({i+1}/10)")
            time.sleep(3)

if __name__ == "__main__":
    start_inventory_service()

import pika
import json
import time
from config import settings

def send_notification(ch, method, properties, body):
    data = json.loads(body)
    order_id = data.get("order_id")
    
    print(f" [✉️] Odesílám potvrzovací e-mail pro objednávku č. {order_id}...")
    time.sleep(1) # Simulace odesílání
    print(f" [✅] E-mail pro objednávku {order_id} odeslán!")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_notifications_service():
    for i in range(10):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.rabbitmq_host))
            channel = connection.channel()

            # Musí být stejná ústředna jako v Orders a Inventory
            channel.exchange_declare(exchange='order_events', exchange_type='fanout')
            
            # Každá služba potřebuje VLASTNÍ unikátní frontu
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            
            channel.queue_bind(exchange='order_events', queue=queue_name)

            channel.basic_consume(queue=queue_name, on_message_callback=send_notification)
            print(' [*] Notifications Service běží a čeká na objednávky...')
            channel.start_consuming()
            break
        except Exception:
            print(f" [!] Čekám na RabbitMQ... ({i+1}/10)")
            time.sleep(3)

if __name__ == "__main__":
    start_notifications_service()

import threading

from src.consumer.application.service.message_service import message_listener
from src.consumer.application.service.notification_service import notification_listener

def main():

    try:
        threads = [
            threading.Thread(target=notification_listener),
            threading.Thread(target=message_listener)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down...")
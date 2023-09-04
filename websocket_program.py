import asyncio
import websockets
import json
import time
import ssl
from asyncio import Queue


async def connect_to_raw_messages_ws(queue, max_messages):
    uri = "wss://test-ws.skns.dev/raw-messages"
    ssl_context = ssl.SSLContext()
    ssl_context.verify_mode = ssl.CERT_NONE  # Отключение проверки сертификата
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        message_count = 0
        min_delay = float('inf')  # Инициализация минимальной задержки бесконечностью
        last_message_id = None
        messages_to_send = {}  # Словарь для хранения сообщений, ожидающих отправки
        while message_count < max_messages:
            message_receive_time = time.time()  # Замер времени получения сообщения
            message_str = await websocket.recv()  # Получение сообщения
            message_send_time = time.time()  # Замер времени отправки сообщения
            delay = message_send_time - message_receive_time

            try:
                data = json.loads(message_str)
                message_id = data.get("id")
                message_text = data.get("text")
                if message_id is not None and message_text is not None:
                    # Добавление сообщения в словарь
                    messages_to_send[message_id] = message_text
                    message_count += 1

                    # Обновление минимальной задержки, если она меньше текущей минимальной
                    min_delay = min(min_delay, delay)

                    print(f"Received message with ID {message_id}: {message_text}")
                    print(f"Delay: {delay} seconds")
                    print(f"Min Delay: {min_delay} seconds")

                    # Проверка, можно ли отправить сообщения в упорядоченном порядке
                    while last_message_id is not None and (last_message_id + 1) in messages_to_send:
                        next_message_id = last_message_id + 1
                        next_message_text = messages_to_send.pop(next_message_id)
                        await queue.put((next_message_id, next_message_text))
                        last_message_id = next_message_id
                        print(f"Sent ordered message with ID {next_message_id}: {next_message_text}")
            except json.JSONDecodeError:
                print("Received invalid JSON message.")

            print(f"Processed {message_count}/{max_messages} messages")  # Отображение текущего прогресса


async def send_ordered_messages(candidate_surname, queue):
    uri = f"wss://test-ws.skns.dev/ordered-messages/{candidate_surname}"
    ssl_context = ssl.SSLContext()
    ssl_context.verify_mode = ssl.CERT_NONE  # Отключение проверки сертификата
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        start_time = time.time()  # Замер времени начала отправки сообщений
        retry_limit = 3  # Максимальное количество попыток отправки одного сообщения
        while True:
            # Получение следующего упорядоченного сообщения из очереди
            message_id, message_text = await queue.get()
            ordered_message = {"id": message_id, "text": message_text}

            # Попытка отправки
            for _ in range(retry_limit):
                try:
                    await websocket.send(json.dumps(ordered_message))
                    print(f"Sent ordered message with ID {message_id}: {message_text}")
                    break  # Успешная отправка, выходим из цикла
                except websockets.exceptions.ConnectionClosedError:
                    # Обработка закрытого соединения
                    print("WebSocket connection closed. Retrying...")
                    await asyncio.sleep(1)  # Пауза перед следующей попыткой

            if message_id == 1000:
                break  # Завершить отправку после достижения лимита
        end_time = time.time()  # Замер времени окончания отправки сообщений
        elapsed_time = end_time - start_time
        print(f"Time taken to send all ordered messages: {elapsed_time} seconds")
        print("All messages sent!")  # Сообщение об окончании отправки


async def main():
    max_messages = 1000  # Установите желаемое количество сообщений для обработки
    queue = Queue()

    # Запросить у пользователя значение candidate_surname
    candidate_surname = input("Введите вашу фамилию: ")

    try:
        raw_messages_task = asyncio.create_task(connect_to_raw_messages_ws(queue, max_messages))
        ordered_messages_task = asyncio.create_task(send_ordered_messages(candidate_surname, queue))

        await asyncio.gather(raw_messages_task, ordered_messages_task)
    except asyncio.CancelledError:
        # ХЗ
        pass


if __name__ == "__main__":
    asyncio.run(main())

#python websocket_program.py

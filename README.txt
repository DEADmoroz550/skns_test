Дорогой читатель, перед нами была поставлена задача:

Test Scenario:
* The candidate develops a program to efficiently send ordered messages from the WebSocket wss://test-ws.skns.dev/raw-messages to wss://test-ws.skns.dev/ordered-messages/{{candidate_surname}}.
* The candidate ensures that the program connects to wss://test-ws.skns.dev/raw-messages as a WebSocket client and receives messages in real-time.
* The messages received from wss://test-ws.skns.dev/raw-messages follow the format {"id": int, "text": int}, where "id" represents the message ID and "text" represents the message content.
* The "id" field of the messages is NOT guaranteed to be in order, and some messages may arrive with random delays.
* The candidate's program should efficiently order the messages based on their IDs and send them to wss://test-ws.skns.dev/ordered-messages/{{candidate_surname}} as soon as possible.
Note: ALL messages in output have to be sorted
* The program should process a minimum of N > 1000 (as the candidate sees fit) messages for testing.
* The candidate's program should measure the time taken to send all ordered messages to wss://test-ws.skns.dev/ordered-messages/{{candidate_surname}}.
* The candidate ensures that the minimum delay between receiving a message from wss://test-ws.skns.dev/raw-messages and sending it to wss://test-ws.skns.dev/ordered-messages/{{candidate_surname}} is recorded.
* The candidate validates that all N messages are sent in the correct order (based on their "id" field) to wss://test-ws.skns.dev/ordered-messages/{{candidate_surname}}.

Инструкция по выполнению/логике:

Импортируйте необходимые модули:
asyncio: Для асинхронной обработки задач.
websockets: Для работы с WebSocket.
json: Для разбора и создания JSON-сообщений.
time: Для измерения времени и задержек.
Определите функции для обработки задач:
connect_to_raw_messages_ws: Эта функция устанавливает соединение с wss://test-ws.skns.dev/raw-messages, получает сообщения и добавляет их в очередь. Также в этой функции измеряется задержка между получением и отправкой сообщений.
send_ordered_messages: Эта функция устанавливает соединение с wss://test-ws.skns.dev/ordered-messages/{{candidate_surname}} и отправляет упорядоченные сообщения на основе их "id". Она также измеряет время отправки всех сообщений.
main: Основная функция, которая создает асинхронные задачи для обработки полученных сообщений и отправки упорядоченных сообщений.
В функции connect_to_raw_messages_ws, в цикле while, вы будете получать сообщения с сервера wss://test-ws.skns.dev/raw-messages, а затем разбирать их, измерять задержку и добавлять в очередь для дальнейшей обработки. Проверка порядка сообщений осуществляется с использованием last_message_id.
В функции send_ordered_messages, также в цикле while, вы будете отправлять упорядоченные сообщения на сервер wss://test-ws.skns.dev/ordered-messages/{{candidate_surname}} на основе данных из словаря, который содержит полученные сообщения. Вы также измеряете время начала и окончания отправки, а также выводите минимальную задержку.
Главная функция main создает очередь и словарь для хранения сообщений и создает две асинхронные задачи: одну для обработки полученных сообщений (connect_to_raw_messages_ws) и вторую для отправки упорядоченных сообщений (send_ordered_messages).

! Запустите цикл выполнения событий asyncio.run(main()) для начала выполнения программы !
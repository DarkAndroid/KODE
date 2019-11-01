Необходимо установить Python 3.x и все необходимые библиотеки из файла requirements.txt
Так же в файле api.py требуется вписать свои данные в кавычки:
alphavantageAPIkey='' # YOUR alphavantage API key ####################################
mymail = '' # YOUR MAIL.RU E-MAIL ####################################
password ='' # YOUR PASSWORD ####################################

Для добавления подписки по тикеру можно отправить запрос следующего содержания (пример для curl для запуска в командной строке):
curl -i -H "Content-Type: application/json" -X POST -d "{ """ticker""": """PINS""", """email""": """mail@example.com""", """max_price""": """25.14""", """min_price""": """25.14""" }" http://localhost:5000/subscription

Для удаления подписки можно отправить запрос следующего содержания (пример для curl для запуска в командной строке):
curl -i -H "Content-Type: application/json" -X DELETE -d "{ """ticker""": """TSLA""", """email""": """mail@example.com"""}" http://localhost:5000/unsubscription

Проверка изменений производится каждый час. В случае обнаружения изменений производится отправка уведомления на email.


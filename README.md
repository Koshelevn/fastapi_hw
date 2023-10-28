# fastapi_hw
Автор: Никита Кошелев

Задача: Реализовать микросервис для хранения и обновления информации для собак!

Endpoints:

GET / возвращает 200

POST /post записывает текущий timestamp в базу и возвращает сущность Timestamp

GET /dog принимает название вида собак и возвращается всех собак указанного вида

POST /dog принимает данные о собаке, записывает в базу и возвращает в ответе

GET /dog/{pk} принимает PRIMARY KEY и возвращает данные о собаке по этому ключу

PATCH /dog/{pk} принимает PRIMARY KEY и данные о собаке, обновляет данные в таблице и возвращает новые данные о собаке.
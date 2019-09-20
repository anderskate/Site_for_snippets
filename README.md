# Приложение для создания сниппетов

Приложение позволяет работать со сниппетами(фрагментами кода). Можно создавать сниппет из нескольких фрагментов кода, а также сделать его не публичным. Фрагменты кода добавляются тремя способами: через текстовое поле, загрузку файла кода или укзания прямой ссылки на скачивание файла.


### Как запустить

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Сделайте миграцию базы данных командами `python3 manage.py makemigrations` и
`python3 manage.py migrate`
- Запустите сервер командой `python3 manage.py runserver`


### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следующие переменные:
- `DEBUG` — дебаг-режим. Поставьте значение TRUE, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта
- `DB_NAME` - название БД 
- `USER` - Логин пользователя для БД
- `PASSWORD`: Пароль пользователя для БД
- `HOST`: Адрес, где находится БД
- `PORT`: Порт для БД


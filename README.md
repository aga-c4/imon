## Инцидент мониторинг

Для запуска потребуется python 3.x, Git, Docker

Перед запуском:

1. Запустите ./install.sh, в результате будут созданы:
- docker-compose.yml на базе docker-compose.sample.yml
- config.py на базе config.sample.py
- app/bin/imon.sh на базе app/bin/imon.sh.sample
Подправьте их под ваши нужды, укажите параметры доступа к БД и другие параметры в config.py
При наличии указанных выше обязательных файлов, они не пересоздадутся. 
Для изменения прав на директории в volumes запустите повторно скрипт под root
2. Создайте необходимые cron скрипты на базе примеров из app/bin/
3. Запустите проект
```
docker-compose up -d
```
3. Зайдите в phpMyAdmin создайте таблицу imon на базе примера из dumps
4. Остановите проект
```
docker-compose down
```
После формирования папки volumes/grafana скопируйте в нее файл базы графаны из папки dumps и поменяйте ему пользователя
```
cp dumps/clear/grafana.db volumes/grafana/grafana.db
chown 472 volumes/grafana/grafana.db
```
Для изменения прав можете просто запустить под root скрипт ./install.sh

Для большей безопасности установите в mysql пароли пользователей кроме root, определите им права и работайте под ними

Для запуска проекта необходимо в таблице metric_projects задать 
проекты метрик, заполнить таблицу metrics. Если нужен инцидент мониторинг, то 
заполнить таблицу tasks, это можно сделать автоматически (смотри помощь основного скрипта)

Пароль к Grafana admin/admin , измените его в целях безопасности

## Полезно:
- Для смены пароля админа Grafana 
```
docker exec -it <имя контейнера Grafana> grafana-cli admin reset-admin-password <новый пароль>
```
- Смена пароля root Mysql в docker-compose.yml
- Интересная статья по настройке VS Code https://habr.com/ru/companies/ruvds/articles/717110/
- Инициализация виртуального окружения в папке app проекта
```
cd app
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


## TODO:
1. Управление таймфреймами из конфига.
2. Управление сообщениями msg_link1 из конфига (робот тваном).


Установка
chown 472:root volumes/grafana

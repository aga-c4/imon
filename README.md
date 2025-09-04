## Инцидент мониторинг

Для запуска потребуется python 3.9+, Git, Docker

Перед запуском:

1. Запустите ./install.sh, в результате будут созданы:
- docker-compose.yml на базе docker-compose.sample.yml
- config.py на базе config.sample.py
- app/bin/imon.sh на базе app/bin/imon.sh.sample
Подправьте их под ваши нужды, укажите параметры доступа к БД и другие параметры в config.py
При наличии указанных выше обязательных файлов, они не пересоздадутся. 
Для изменения прав на директории в volumes запустите повторно скрипт под root, при этом выполнится
```
sudo chown 472:root volumes/grafana
```
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
sudo chown 472 volumes/grafana/grafana.db
```
Для изменения прав можете просто запустить под root скрипт sudo ./install.sh

Для большей безопасности установите в mysql пароли пользователей кроме root, определите им права и работайте под ними

Для запуска проекта необходимо в таблице metric_projects задать 
проекты метрик, заполнить таблицу metrics. Если нужен инцидент мониторинг, то 
заполнить таблицу tasks, это можно сделать автоматически (смотри помощь основного скрипта)

Пароль к Grafana admin/admin , измените его в целях безопасности
Пароль к MySQL root/root , измените его в целях безопасности

Зайдите в phpMyAdmin или иным способом создайте БД imon с кодировкой utf8mb4_general_ci
на базе файла dumps/clear/imon_clear.sql

Если необходимо запустить python процесс не с хостовой машины, а под Docker, то
выполните следующую команду из app проекта:
```
docker build -t imon .
```
далее вы сможете запускать контейнер с Python командой
```
./dockerimon.sh [Command1] [Param1] [Command2] [Param2] ...
```
запустите без параметров, для получения справки.

Для очистки tmp выполните из корня проекта
./dockercleartmp.sh (через запуск контейнера)
./app/bin/cleartmp.sh (на хостовой машине)

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
- Посмотреть доступные сети в Docker можно так
```
docker inspect c1 -f "{{json .NetworkSettings.Networks }}"
```

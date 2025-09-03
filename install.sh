#!/bin/bash

# Переход в директорию, где расположен скрипт
cd "$(dirname "$0")"

if [ ! -d "volumes/mysql" ]; then
  mkdir "volumes/mysql"
  echo "Create volumes/mysql"
fi
if [ ! -d "volumes/grafana" ]; then
  mkdir "volumes/grafana"
  echo "Create volumes/grafana"
fi
chown 472 volumes/grafana

if [ ! -f "docker-compose.yml" ]; then
  cp "docker-compose.sample.yml" "docker-compose.yml"
  echo "Create docker-compose.yml from docker-compose.sample.yml"
fi

if [ ! -f "app/config.py" ]; then
  cp "app/config.sample.py" "app/config.py"
  echo "Create config.py from config.sample.py"
fi

if [ ! -f "app/bin/imon.sh" ]; then
  cp "app/bin/imon.sh.sample" "app/bin/imon.sh"
  echo "Create app/bin/imon.sh from app/bin/imon.sh.sample"
fi

if [ ! -f "app/bin/cleartmp.sh" ]; then
  cp "app/bin/cleartmp.sh.sample" "app/bin/cleartmp.sh"
  echo "Create app/bin/cleartmp.sh from app/bin/cleartmp.sh.sample"
fi

#!/bin/sh
array="${@}"
docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest /bin/bash ./bin/cron_w1.sh

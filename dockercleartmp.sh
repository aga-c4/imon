#!/bin/sh

docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest python /bin/bash bin/cleartmp.sh

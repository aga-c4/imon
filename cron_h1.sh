#!/bin/sh
array="${@}"
docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest python imon.py  runrobot --log_view INFO --robot getload --source b2bcur  --project_id 1
docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest python imon.py  runrobot --log_view INFO --robot getload --source b2bstab --project_id 2
docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest python imon.py  runrobot --log_view INFO --robot getload --source shrib2b --project_id 3
docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest python imon.py  runrobot --log_view INFO --robot getload --source shriho  --project_id 4
docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest python imon.py  mgen --granularity m1
docker run -ti --rm --network imon_my-net -v $(pwd)/app:/usr/src/app  -w /usr/src/app imon:latest python imon.py  mgen --granularity h1

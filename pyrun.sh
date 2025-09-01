#!/bin/sh
array="${@}"
docker run -ti --rm -v $(pwd)/app/www:/var/www -v $(pwd)/docker/images/php/conf.d.dev:/usr/local/etc/php/conf.d -v $(pwd)/docker/images/php/php-fpm.d/zzz-01-add.conf:/usr/local/etc/php-fpm.d/zzz-01-add.conf -v $(pwd)/docker/images/php/openssl.cnf:/etc/ssl/openssl.cnf -w /var/www agac4/inc_php8.2-fpm-sqlsrv:latest $array

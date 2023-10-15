#!/bin/bash

docker run \
  --privileged \
  --hostname=1845ab38a1eb \
  --user=tshark-user \
  --mac-address=02:42:ac:11:00:02 \
  --env PATH=/opt/rabbitmq/sbin:/opt/erlang/bin:/opt/openssl/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  --env ERLANG_INSTALL_PATH_PREFIX=/opt/erlang \
  --env OPENSSL_INSTALL_PATH_PREFIX=/opt/openssl \
  --env RABBITMQ_DATA_DIR=/var/lib/rabbitmq \
  --env RABBITMQ_VERSION=3.12.6 \
  --env RABBITMQ_PGP_KEY_ID=0x0A9AF2115F4687BD29803A206B73A36E6026DFCA \
  --env RABBITMQ_HOME=/opt/rabbitmq \
  --env HOME=/var/lib/rabbitmq \
  --env LANG=C.UTF-8 \
  --env LANGUAGE=C.UTF-8 \
  --env LC_ALL=C.UTF-8 \
  --volume=/var/lib/rabbitmq \
  -p 15671 \
  -p 15672 \
  -p 15691 \
  -p 15692 \
  -p 25672 \
  -p 4369 \
  -p 5671 \
  -p 5672 \
  --label='org.opencontainers.image.ref.name=ubuntu' \
  --label='org.opencontainers.image.version=22.04' \
  --runtime=runc \
  -d \
  leq2019/rabbitmq-with-terminal-shark:latest
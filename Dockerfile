#
# Haproxy Dockerfile
#
# https://github.com/dockerfile/haproxy
#

FROM haproxy:1.7
COPY haproxy.cfg /etc/haproxy/haproxy.cfg

#FROM ubuntu
#
## Install Haproxy.
#RUN \
#  sed -i 's/^# \(.*-backports\s\)/\1/g' /etc/apt/sources.list && \
#  apt-get update && \
#  apt-get install -y haproxy && \
#  sed -i 's/^ENABLED=.*/ENABLED=1/' /etc/default/haproxy && \
#  rm -rf /var/lib/apt/lists/*
#
## Add files.
#ADD haproxy.cfg /etc/haproxy/haproxy.cfg
#ADD start.bash /haproxy-start
#
## Define mountable directories.
#VOLUME ["/haproxy-override"]
#
## Define working directory.
#WORKDIR /etc/haproxy
#
## Define default command.
#CMD bash
#CMD /haproxy-start
#
## Expose ports.
#EXPOSE 80
#EXPOSE 443
FROM debian:8.6

RUN apt-get update
RUN apt-get -y --no-install-recommends install memcachedb

EXPOSE 21201

ENTRYPOINT ["/usr/bin/memcachedb", "-m", "64", "-p", "21201", "-A", "4096", "-u", "memcachedb", "-l", "0.0.0.0", "-H", "/var/lib/memcachedb", "-f", "/var/lib/memcachedb/default.db", "-U", "off"]
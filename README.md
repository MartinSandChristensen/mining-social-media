# Mining social media for fun and profit

This is the companion code and configuration to my article series of
the same name. It will spin up a few Docker containers that will pull
data from Twitter, send tweets to a RabbitMQ message queue which will
in turn send them to two services: the first is permanent storage in
an ElasticSearch database, and the second is a tweet parser. The
parser then sends the parsed message to a new message queue, and from
there it will be consumed by a classification service.



## How to run

First, set up docker

sysctl -w vm.max_map_count=262144

Edit "run" file


## Containers

elasticsearch
  Runs our ElasticSearch data store.

rabbitmq
  Our message queue middleware instance.

elasticfeeder
  This runs a service that takes raw tweets from a queue and feeds them into ElasticSearch.

tweetparser
  Runs a service that grabs raw tweets from a queue, tokenises them
  and puts them on another queue.

slurp
  This service grabs data from the Twitter stream.


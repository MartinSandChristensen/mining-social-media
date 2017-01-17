# Mining social media for fun and profit

This is the companion code and configuration to my article series of
the same name. It will spin up a few Docker containers that will pull
data from Twitter, send tweets to a RabbitMQ message queue which will
in turn send them to two services: the first is permanent storage in
an CouchDB database, and the second is a tweet parser. The parser then
sends the parsed message to a new message queue, and from there it
will be consumed by a classification service.

Be warned that it's a work in progress.


## How to run

First, set up Docker. On Debian or Ubuntu, "sudo apt install
docker.io" will do the trick. For your platform of choice, see the
Docker web site for documentation.

To get access to Twitter's stream, create an app at
https://apps.twitter.com/ and name it however you like. Under that
app, go to the Keys and Access Tokens tab. Here you'll find your
Consumer Key and Consumer Secret. Further down on the page you need to
click Create my access token. This will generate an Access Token and
Access Token Secret. You need all four of these keys. In the
mining-social-media directory (here), create a file called
twitter.env, which should look something like this:

    CONSUMER_KEY=FkiG5ILCsYYEUTnmyBkA5KBO4
    CONSUMER_SECRET=JkPzOkW97lwSfgnz9UVibshMrt9AxezyaIjNyPN2LSh1ihPw4D
    ACCESS_TOKEN=3251707498-IH2MbaIEK7eL2zDULBcF2AcdVGrWm1xtIgTDka4
    ACCESS_TOKEN_SECRET=DL3e72EtsobnfkNgyFFSAOC0Cjv2ex3n3u4SqSRp8ORnj
    TRACK='["trump", "clinton"]'

but of course substitute these (fake) keys for your own. The TRACK
variable can be set to whatever search parameters you'd like.

Now you should be able to execute the run file from the shell. This
will create the required Docker images and spin up containers. After
the first time, you should start the containers you want by hand.

Why not Docker Compose? Well, it's sort of on its way, I think, but
since it's not supported on even newer versions on several of the more
widely used Linux distros, I'm not making it a priority.


## Containers

- `couchdb`: Runs our CouchDB data store.
- `rabbitmq`: Our message queue middleware instance.
- `couchfeeder`: This runs a service that takes raw tweets from a queue and feeds them into CouchDB.
- `tweetparser`: Runs a service that grabs raw tweets from a queue, tokenises them and puts them on another queue.
- `tweetfetcher`: This service grabs data from the Twitter stream.
- `filestreamer`: Store tweets in flat files, one tweet per line and in compressed archives of, by default, 10,000 per file.
- `memcachedb`: MemcacheDB service, not integrated yet.

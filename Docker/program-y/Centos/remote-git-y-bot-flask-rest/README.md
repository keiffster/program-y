# Docker Config File

This was created by user [@ohoachuck](https://github.com/ohoachuck)

His notes/comments are as follows :-


I have successfully created a container with Centos linux distribution + Python 3.6 + Program-y. And have uploaded to Docker Store what I believe should be testable by anybody in a minute (given that you have docker installed). Unless something goes wrong, it should be as simple as doing:
```bash
docker pull ohoachuck/program-y-git-y-bot-webchat
docker run -t -i -p 80:80 ohoachuck/program-y-git-y-bot-webchat
```
to do so I did nothing complicated, and just wrote a simple Dockerfile

This first Docker exploration might motivate some more experimented folks to move on this ? At least I hope this could help go a bit forward. I will continue my explorations.

## Build your own image

You can customise the provided simple Dockerfile and build your own image. To do so make sure you are in directory where Dockerfile is. And use docker basic command CLI:
```bash
docker build -t <your-prefered-image-name> .
```

## Run your own container from image

Once you have built your own imgage run your container for access through port 80 (http://localhost) like so:
```bash
docker run -t -i -p 8080:80 <your-prefered-image-name>
```
or alternatively you can choose to map same PORT as the container port 8080 (http://localhost:8080) like so:
```bash
docker run -t -i -p 8080:8080 <your-prefered-image-name>
```

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
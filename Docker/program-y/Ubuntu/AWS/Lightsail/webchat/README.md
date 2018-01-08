# Docker Config File

This configuration file will create a Docker image this is as identical 
as I can get it to an AWS Ubuntu 16.04 LTS install as used on AWS Lightsail instance

This is the same AWS configuration that I use for hosting Program-Y on AWS at
[Program-y Demonstration](http://35.176.114.251:8080/)

To use it, first ensure you have Docket installed, and then create an immage
```bash
docker build -t program-y .
```
Once you have an image, you can create an instance from the image
```bash
docker run --detach --privileged --name program-y -v /sys/fs/cgroup:/sys/fs/cgroup -p 8080:8080 program-y
```

This instance was developed on the back of the work by Kevin Coakley
https://hub.docker.com/r/kevincoakley/ubuntu16.04-systemd/ because AWS Ubuntu installs 
uses systemd to control services, and the default Ubuntu docket install doesn't ship with it

Anyway, enjoy and if it doesn't work blame Kevin lol, no seriously blame Kevin I totally ripped this off his site!
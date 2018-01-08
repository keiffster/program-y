FROM ubuntu:16.04

ENV container docker

RUN systemctl set-default multi-user.target

RUN apt-get update; apt-get -y install openssh-server openssh-client; apt-get clean
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo 'root:docker' | chpasswd
RUN systemctl enable ssh.service

VOLUME ["/sys/fs/cgroup"]
VOLUME ["/run"]

RUN \
  echo Installing dev tools && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y software-properties-common && \
  apt-get install -y build-essential && \
  apt-get install -y git

RUN \
  echo Installing Python 3.6 && \
  add-apt-repository ppa:jonathonf/python-3.6 && \
  apt-get update && \
  apt-get install -y python3.6 && \
  rm /usr/bin/python3 && \
  ln -s /usr/bin/python3.6 /usr/bin/python3

RUN \
  echo installing Pip 3 && \
  apt-get install -y python3-pip && \
  pip3 install --upgrade pip

RUN mkdir /opt/program-y

WORKDIR /opt/program-y

RUN \
  echo Installing Program-y && \
  git init . && \
  git remote add program-y https://github.com/keiffster/program-y && \
  git pull program-y master && \
  pip3 install -r requirements.txt

CMD ["/sbin/init"]

RUN useradd -ms /bin/bash ubuntu
RUN chown -R ubuntu.ubuntu /opt/program-y

RUN echo Installing program-y as a service
RUN cp /opt/program-y/bots/y-bot/servusai.service /etc/systemd/system/servusai.service 
RUN chmod +x /opt/program-y/bots/y-bot/servusai.sh
RUN systemctl enable servusai.service 

EXPOSE 8080
EXPOSE 22



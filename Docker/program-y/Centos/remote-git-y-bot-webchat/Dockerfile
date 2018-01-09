############################################################
# Dockerfile to build program-y Application Containers
# Based on centos and python 3.6
############################################################

# Set the base image to centos
FROM centos

# File Author / Maintainer
MAINTAINER Olivier HO-A-CHUCK

# Update the sources list
RUN yum update -y

# Install basic applications
RUN yum install -y tar git curl nano wget dialog net-tools yum-utils

# Install Python and Basic Python Tools
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python36u python36u-pip python36u-devel

# link python3.6 to python3
RUN ln -s /usr/bin/python3.6 /usr/bin/python3

# create program-y user with password=program-y
RUN useradd -m -p program-y program-y

# get program-y repo source as "program-y" user (could be your own repo with you own bot implementation)
RUN su -c 'git clone https://github.com/keiffster/program-y.git /home/program-y/program-y' - program-y

# Get pip to download and install requirements:
RUN pip3.6 install -r /home/program-y/program-y/requirements.txt

# Expose ports for webchat if launched as program-y user
EXPOSE 8080

# Copy the launch script inside the container
# launch.sh is : su -c 'cd /home/program-y/program-y/bots/y-bot/ && /home/program-y/program-y/bots/y-bot/y-bot-webchat.sh' - program-y
ADD /launch.sh /home/program-y/program-y/bots/y-bot/launch.sh

# Set the default directory where CMD will execute
WORKDIR /home/program-y/program-y/bots/y-bot/

# Set the default command to execute
# when creating a new container
# Launch y-bot-webchat.sh as user "program-y"
CMD /bin/bash ./launch.sh
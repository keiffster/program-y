#!/bin/sh
# chkconfig: 123456 90 10
# Programy Web Chat Client
#

workdir=/home/ec2-user/programy
export PYTHONPATH=$workdir/src:$workdir/libs/MetOffer-1.3.2:.

start() {
    cd $workdir
    /usr/bin/python $workdir/clients/webchat/chatsrv.py --config $workdir/bots/y-bot/config.yaml --cformat yaml --logging $workdir/bots/y-bot/logging.yaml &
    echo "Server started."
}

stop() {
    pid=`ps -ef | grep '/programy/src/clients/webchat/chatsrv.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: /etc/init.d/programy-webchat.sh {start|stop|restart}"
    exit 1
esac
exit 0

#! /bin/sh

systemctl restart servusai-rest.service

systemctl start servusai-web.service

#systemctl restart servusai-facebook.service
#systemctl restart servusai-kik.service
#systemctl restart servusai-line.service
#systemctl restart servusai-slack.service
#systemctl restart servusai-socket.service
#systemctl restart servusai-telegram.service
#systemctl restart servusai-twilio.service
#systemctl restart servusai-twitter.service
# systemctl start servusai-viber.service
#systemctl start servusai-xmpp.service

journalctl -xe

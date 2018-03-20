#! /bin/sh

cp servusai-xmpp.service /etc/systemd/system/servusai-xmpp.service
systemctl daemon-reload
systemctl enable servusai-xmpp.service
systemctl start servusai-xmpp.service
systemctl status servusai-xmpp.service
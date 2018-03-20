#! /bin/sh

cp servusai-twitter.service /etc/systemd/system/servusai-twitter.service
systemctl daemon-reload
systemctl enable servusai-twitter.service
systemctl start servusai-twitter.service
systemctl status servusai-twitter.service
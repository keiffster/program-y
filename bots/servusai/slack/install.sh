#! /bin/sh

cp servusai-slack.service /etc/systemd/system/servusai-slack.service
systemctl daemon-reload
systemctl enable servusai-slack.service
systemctl start servusai-slack.service
systemctl status servusai-slack.service
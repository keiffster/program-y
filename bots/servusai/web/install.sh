#! /bin/sh

cp servusai-web.service /etc/systemd/system/servusai-web.service
systemctl daemon-reload
systemctl enable servusai-web.service
systemctl start servusai-web.service
systemctl status servusai-web.service
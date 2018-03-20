#! /bin/sh

cp servusai-viber.service /etc/systemd/system/servusai-viber.service
systemctl daemon-reload
systemctl enable servusai-viber.service
systemctl start servusai-viber.service
systemctl status servusai-viber.service
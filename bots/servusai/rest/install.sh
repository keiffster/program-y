#! /bin/sh

cp servusai-rest.service /etc/systemd/system/servusai-rest.service
systemctl daemon-reload
systemctl enable servusai-rest.service
systemctl start servusai-rest.service
systemctl status servusai-rest.service
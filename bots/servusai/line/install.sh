#! /bin/sh

cp servusai-line.service /etc/systemd/system/servusai-line.service
systemctl daemon-reload
systemctl enable servusai-line.service
systemctl start servusai-line.service
systemctl status servusai-line.service
#! /bin/sh

cp servusai-socket.service /etc/systemd/system/servusai-socket.service
systemctl daemon-reload
systemctl enable servusai-socket.service
systemctl start servusai-socket.service
systemctl status servusai-socket.service
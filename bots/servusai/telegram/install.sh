#! /bin/sh

cp servusai-telegram.service /etc/systemd/system/servusai-telegram.service
systemctl daemon-reload
systemctl enable servusai-telegram.service
systemctl start servusai-telegram.service
systemctl status servusai-telegram.service
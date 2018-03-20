#! /bin/sh

cp servusai-facebook.service /etc/systemd/system/servusai-facebook.service
systemctl daemon-reload
systemctl enable servusai-facebook.service
systemctl start servusai-facebook.service
systemctl status servusai-facebook.service
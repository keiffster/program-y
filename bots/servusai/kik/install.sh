#! /bin/sh

cp servusai-kik.service /etc/systemd/system/servusai-kik.service
systemctl daemon-reload
systemctl enable servusai-kik.service
systemctl start servusai-kik.service
systemctl status servusai-kik.service
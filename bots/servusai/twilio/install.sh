#! /bin/sh

cp servusai-twilio.service /etc/systemd/system/servusai-twilio.service
systemctl daemon-reload
systemctl enable servusai-twilio.service
systemctl start servusai-twilio.service
systemctl status servusai-twilio.service
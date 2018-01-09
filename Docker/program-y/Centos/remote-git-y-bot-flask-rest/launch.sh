#!/bin/bash

# Run python sever as program-y user (not root)
`su -c 'cd /home/program-y/program-y/bots/y-bot/ && /home/program-y/program-y/bots/y-bot/y-bot-flask-rest.sh' - program-y`
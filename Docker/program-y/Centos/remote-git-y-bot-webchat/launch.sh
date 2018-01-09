#!/bin/bash

# Run python sever as program-y user (not root)
#`su -c 'cd /home/program-y/program-y/bots/y-bot/ && /home/program-y/program-y/bots/y-bot/y-bot-webchat.sh' - program-y`

# Launch Program-y as root, unless default config.yaml file state webchat port is greater than 1024 (ex. 8080)
`cd /home/program-y/program-y/bots/y-bot/ && /home/program-y/program-y/bots/y-bot/y-bot-webchat.sh`
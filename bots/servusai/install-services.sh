#! /bin/sh

cd rest
install-services.sh

cd ../web
install-services.sh

cd ../facebook
./install.sh

cd ../kik
./install.sh

cd ../line
./install.sh

cd ../slack
./install.sh

cd ../socket
./install.sh

cd ../telegram
./install.sh

cd ../twilio
./install.sh

cd ../twitter
./install.sh

# cd ../viber
# ./install.sh

cd ../xmpp
./install.sh

journalctl -xe





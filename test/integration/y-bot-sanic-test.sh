#! /bin/sh

clear

curl 'http://localhost:8989/api/v1.0/ask?question=do+you+know+holly+from+red+dwarf&sessionid=1234567890'
echo ""

curl 'http://localhost:8989/api/v1.0/ask?question=yes&sessionid=1234567890'

#! /bin/sh

clear

curl 'http://localhost:8989/api/rest/v1.0/ask?question=do+you+know+holly+from+red+dwarf&sessionid=1234567890&userid=1'
echo ""

curl 'http://localhost:8989/api/rest/v1.0/ask?question=yes&sessionid=1234567890&userid=1'

# client.py
import socket
import sys
import json

host =      sys.argv[1]
port =      int(sys.argv[2])
question =  sys.argv[3]
userid =  sys.argv[4]
max_size =  1024
if len(sys.argv) == 6:
    max_size = sys.argv[5]

payload = {"question": question, "userid": userid}
json_data = json.dumps(payload)

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connection to hostname on the port.
s.connect((host, port))

s.send(json_data.encode('utf-8'))

# Receive no more than 1024 bytes
received = s.recv(max_size)

s.close()

json_data = json.loads(received.decode('utf-8'))

print("Answer: %s" % json_data['answer'])

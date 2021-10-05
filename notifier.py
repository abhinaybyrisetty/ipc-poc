from __future__ import print_function
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("localhost")
s.bind((host, 8800))
s.listen(5)
conn, addr = s.accept()
while True:
  conn, addr = s.accept()
  data = conn.recv(1024)
  print(data)
  if not data:
    conn.close()

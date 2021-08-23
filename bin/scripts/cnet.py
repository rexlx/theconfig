import socket

s = socket.socket()
host = socket.gethostname()
port = 41000

s.connect((host, port))
s.send(str(host) + " connected...")

with open('file', 'wb') as f:
    print('file opened...')
    while True:
        print('getting data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        f.write(data)
f.close()
print('xfer complete...')
s.close()
print('connection severed...')


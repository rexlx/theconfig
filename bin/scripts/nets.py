import socket

port = 41000
s = socket.socket()
host = socket.gethostname()
s.bind((host, port))
s.listen(5)

print("server listening on: " + str(port))

while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    print("talking to " + str(addr))
    print("got: " + repr(data))

    filename = 'hosts'
    f = open(filename, 'rb')
    l = f.read(1024)
    while (l):
        conn.send(l)
        print("xfer complete " + repr(l))
        l = f.read(1024)
    f.close()

    print('complete...')
    conn.send("xfer complete, thanks :)")
    conn.close()


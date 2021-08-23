import socket, platform

def get_dist():
    dist = platform.linux_distribution()
    x = ' '.join(e for e in dist)
    return x

hostname = socket.gethostname()
os = get_dist()

print(hostname.ljust(36) + os)



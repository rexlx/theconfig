import socket, sys


def nslookup(target):
    ip_list = []
    ips = socket.getaddrinfo(target,0,0,0,0)
    for ip in ips:
        ip_list.append(ip[-1][0])
        ip_list = list(set(ip_list))
    return ip_list

def get_args():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        return target
    else:
        print("expected a hostname!")

def main():
    target = get_args()
    results = nslookup(target)
    print(results)

if __name__ == '__main__':
    main()

import os
import getpass
import paramiko as pm

home_dir = os.path.expanduser('~')
key = home_dir + '/.ssh/id_rsa'
pkey = pm.RSAKey.from_private_key_file(key)
#addr = 'rxcl2'
addr = '192.168.1.87'
# auth = {'uname': 'rxlx', 'upwd': 'upwd', 'rpwd': 'rpwd', 'port': 22}


def get_auth(is_pwd=False):
    if is_pwd:
        rpwd = getpass.getpass(prompt="enter your root pwd")
        upwd = getpass.getpass(prompt="enter your user pwd")
        auth = {'uname': 'rxlx', 'upwd': upwd, 'rpwd': rpwd,
                'key': False, 'addr': addr, 'port': 22}
    else:
        auth = {'uname': 'rxlx', 'upwd': None, 'rpwd': None,
                'key': pkey, 'port': 22}
    return auth


def ssh(auth, command):
    try:
        client = pm.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(pm.WarningPolicy)
        if auth['key']:
            client.connect(hostname=addr, username=auth['uname'],
                           pkey=auth['key'], port=auth['port'])
        else:
            client.connect(hostname=addr, username=auth['uname'],
                           password=auth['upwd'], port=auth['port'])
        for i in command:
            print("running " + i)
            stdin, stdout, stderr = client.exec_command(i)
            print(stdout.read().split)
            print(stderr.read())
    except Exception as e:
        print("exception!!!", e)
    finally:
        client.close()


def send_cmd():
    cmd_list = ["sudo yum upgrade -y", 'sudo updatedb']
    # cmd_list = ["ls -lrth", "du -sh", "sudo updatedb"]
    auth = get_auth(is_pwd=False)
    ssh(auth, cmd_list)


send_cmd()
# def scp_file(auth, paths):
#     try:
#         transport = pm.Transport((hostname, port))
#         transport.connect(username=auth[uname])

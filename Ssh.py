import time
import sys
import paramiko
import datetime


####################################################################

class Ssh:

    def __init__(self, server_ip, server_port, user, password):
        self.server_ip = server_ip
        self.server_port = server_port
        self.user = user
        self.password = password

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.server_ip,
                                port=self.server_port,
                                username=self.user,
                                password=self.password,
                                look_for_keys=False,
                                allow_agent=False, banner_timeout=200)

        except:
            print(f"unable to establish ssh connection to ip {server_ip}")
            sys.exit(1)

        self.connection = self.client.invoke_shell()

    def send_command(self, command):
        self.connection.send(command + '\n')
        time.sleep(2)
        output = self.connection.recv(4096)
        return output.decode()

    def close(self):
        if self.client.get_transport().is_active():
            self.client.close()

####################################################################
def send_ssh_command(ip, cmd):
    print(f"[{datetime.datetime.now()}] -- send SSH command '{cmd}' to {ip}")
    try:
        ssh_connection = Ssh(ip, 22, "admin", "admin")
        results = ssh_connection.send_command(cmd)
        #print(f">>>>>{results}<<<<<")
        print(f"{results}")
        ssh_connection.close()
    except:
        print(f"SSH command '{cmd}' to {ip} failed")
        sys.exit(2)

def sleep(new_sleep):
    print(f"[{datetime.datetime.now()}] -- sleep {new_sleep:3} sec")
    time.sleep(new_sleep)


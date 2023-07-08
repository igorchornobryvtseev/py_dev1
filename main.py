import time
import sys
import datetime

from Ssh import Ssh
from colorama import Fore, Style


def check_connectivity_after(ip):
    print("check connectivity after\n")
    try:
        ip_connection = Ssh(ip, 22, "admin", "admin")
        ip_connection.close()
    except:
        #print(Fore.RED + "Error, no ssh to {ip} after sending command\nMight be a reboot please check logs" + Style.RESET_ALL)
        print("Error, no ssh\n")
    time.sleep(4 * 60)  # 4 minutes wait after checking if device has connection to ssh
    time.sleep(10)


def set_eth_eth2_eth_type(ip, eth_type, value_prefix, values_arr):
    for val in values_arr:
        try:
            ip_connection = Ssh(ip, 22, "admin", "admin")
            ip_connection.set_eth2(eth_type, val, value_prefix)
            #ip_connection.copy_running_startup()
            ip_connection.close()
            print("ip_connection -- closed")
            time.sleep(10)  # 10 seconds wait after sending command to device
        except:
            #print(Fore.RED + f"Error, no ssh to {ip} before sending command" + Style.RESET_ALL)
            print(f"Error, no ssh to {ip} before sending command")


def send_ssh_command(ip, cmd):
    print(f"send SSH command '{cmd}' to {ip}")
    try:
        ssh_connection = Ssh(ip, 22, "admin", "admin")
        results = ssh_connection.send_command(cmd)
        print(f">>>>>{results}<<<<<")
        ssh_connection.close()
    except:
        print(f"SSH command '{cmd}' to {ip} failed")
        sys.exit(2)

def calculate_sleep(iter_num):
    iter_period = 20
    sleep_min = 30
    sleep_step = 30

    iter_cur = iter_num % iter_period # 1,2,3,4,    0,1,2,3,4, 
    new_sleep = sleep_min + iter_cur * sleep_step

    print(f"iter:{iter_num} sleep:{new_sleep}")


if __name__ == '__main__':

    iteration = 1
    max_iteration = 100
    for iteration in range(1, max_iteration + 1):
    #while iteration <= max_iteration:
        calculate_sleep(iteration)

    sys.exit(0)


    devA_ip = "10.61.117.33"
    max_iteration = 100
    sleep_after_command = 3 * 60

    iteration = 1 
    while iteration <= max_iteration:
        now = datetime.datetime.now()
        print(f"-- Start iteration number {iteration} -- {now}")
        send_ssh_command(devA_ip, "set eth eth2 eth-type rj45 1000fd")
        time.sleep(sleep_after_command)

        send_ssh_command(devA_ip, "set eth eth2 eth-type rj45 10000fd")
        time.sleep(sleep_after_command)

        iteration += 1
    print("DONE")



# #########################
# EH-8010FX-L>show ip

# ip 1 ip-addr                   : dhcp 10.61.118.6
# ip 1 prefix-len                : 24
# ip 1 vlan                      : 0
# ip 1 default-gateway           : 10.61.118.1

# ip 2 ip-addr                   : static 10.61.117.33
# ip 2 prefix-len                : 24
# ip 2 vlan                      : 0
# ip 2 default-gateway           : 0.0.0.0


# EH-8010FX-H>show ip

# ip 1 ip-addr                   : dhcp 10.61.118.5
# ip 1 prefix-len                : 24
# ip 1 vlan                      : 0
# ip 1 default-gateway           : 10.61.118.1

# ip 2 ip-addr                   : static 10.61.118.33
# ip 2 prefix-len                : 24
# ip 2 vlan                      : 0
# ip 2 default-gateway           : 10.61.118.1

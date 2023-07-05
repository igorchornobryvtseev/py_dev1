import time

from Ssh import Ssh
from colorama import Fore, Style


def check_connectivity_after(ip):
    try:
        ip_connection = Ssh(ip, 22, "admin", "admin")
        ip_connection.close()
    except:
        print(Fore.RED + f"Error, no ssh to {ip} after sending command\n"
                         f"Might be a reboot please check logs" + Style.RESET_ALL)
    time.sleep(4 * 60)  # 4 minutes wait after checking if device has connection to ssh


def set_eth_eth2_eth_type(ip, eth_type, value_prefix, values_arr):
    for val in values_arr:
        try:
            ip_connection = Ssh(ip, 22, "admin", "admin")
            ip_connection.show_sw_not_active_version(eth_type, val, value_prefix)
            ip_connection.copy_running_startup()
            ip_connection.close()
            time.sleep(10)  # 10 seconds wait after sending command to device
        except:
            print(Fore.RED + f"Error, no ssh to {ip} before sending command" + Style.RESET_ALL)
        check_connectivity_after(ip)


if __name__ == '__main__':
    # Please update variables #
    ip_arr = ["10.50.105.13", "10.50.105.14"]
    eth_types = ["rj45", "sfp"]  # rj45 has fd value prefix, sfp has xfd value prefix
    values = ["1000", "10000"]
    values_prefix = ["fd", "xfd"]
    # Please update variables #

    # 1 device on link = current master version
    # 2 device on link = Igor's implementation

    iteration = 1
    while iteration < 100:
        print(f"-- Start iteration number {iteration} --")
        for i in range(0, 2):
            set_eth_eth2_eth_type(ip_arr[i], eth_types[i], values_prefix[i], values)
        print(f"-- End iteration number {iteration} --")
        iteration += 1

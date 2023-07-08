import time
import sys
import datetime

from Ssh import send_ssh_command
from Ssh import sleep


def calculate_sleep(sleep_min, sleep_max, sleep_step, iter_num):
    iter_period = (sleep_max - sleep_min) // sleep_step
    iter_cur = iter_num % iter_period
    new_sleep = sleep_min + iter_cur * sleep_step
    return new_sleep


if __name__ == '__main__':

    #iteration = 1

    sleep_min = 30
    sleep_max = 600
    sleep_step = 10
    iter_period = (sleep_max - sleep_min) // sleep_step

    max_iteration = (sleep_max - sleep_min) // sleep_step


    total_time = 0

    devA_ip = "10.61.117.33"

    for iteration in range(1, max_iteration):
        print(f"[{datetime.datetime.now()}] -- Start iteration number {iteration}")

        send_ssh_command(devA_ip, "show eth eth2")

        new_sleep = calculate_sleep(sleep_min, sleep_max, sleep_step, iteration)
        sleep(new_sleep)


        # total_time += new_sleep
        # total_min = total_time // 60
        # print(f"iter:{iteration:4} sleep:{new_sleep:5} total_time:{total_time:5} total_min:{total_min}")

        #send_ssh_command(devA_ip, "show eth eth2")
        #sleep(new_sleep)

    print("DONE")
    sys.exit(0)


    # max_iteration = 100

    # iteration = 1 
    # while iteration <= max_iteration:
    #     now = datetime.datetime.now()
    #     print(f"-- Start iteration number {iteration} -- {now}")
    #     #send_ssh_command(devA_ip, "set eth eth2 eth-type rj45 1000fd")
    #     send_ssh_command(devA_ip, "show eth eth2")
    #     time.sleep(sleep_after_command)

    #     # send_ssh_command(devA_ip, "set eth eth2 eth-type rj45 10000fd")
    #     # time.sleep(sleep_after_command)

    #     iteration += 1
    # print("DONE")

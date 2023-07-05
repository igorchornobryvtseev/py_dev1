import time

import paramiko
from colorama import Fore, Style
from pysnmp import hlapi


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
        pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))
    return pairs


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(),
        context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def get_bulk(target, oids, credentials, count, start_from=0, port=161,
             engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        start_from, count,
        *construct_object_types(oids)
    )
    return fetch(handler, count)


def get_bulk_auto(target, oids, credentials, count_oid, start_from=0, port=161,
                  engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    count = get(target, [count_oid], credentials, port, engine, context)[count_oid]
    return get_bulk(target, oids, credentials, count, start_from, port, engine, context)


def set(target, value_pairs, credentials, port=161, engine=hlapi.SnmpEngine(),
        context=hlapi.ContextData()):
    handler = hlapi.setCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_value_pairs(value_pairs)
    )
    return fetch(handler, 1)[0]


#####################################################################
def check_set_done(response_command):
    if "Set done" in response_command:
        return True
    else:
        return False


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
                                allow_agent=False)

        except:
            print('unable to establish ssh connection')

        self.connection = self.client.invoke_shell()

    def reconnect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.server_ip,
                                port=self.server_port,
                                username=self.user,
                                password=self.password,
                                look_for_keys=False,
                                allow_agent=False)
        except:
            print('unable to establish ssh connection')

    def send_command(self, command):
        self.connection.send(command + '\n')
        time.sleep(2)
        output = self.connection.recv(4096)
        return output.decode()

    def check_frequency_in_units(self):
        command = 'show rf channel-width'
        results = self.send_command(command)
        split_string = results.split(" ")
        my_num1 = split_string[-1]
        channel_width = []
        for i in my_num1[:5]:
            if i.isdigit():
                channel_width.append(i)
            else:
                pass
        num = ''.join(channel_width)
        command2 = "show rf tx-frequency"
        results = self.send_command(command2)
        split_string = results.split(" ")
        my_num2 = split_string[-1]
        the_frequency_tx = []
        for i in my_num2[:5]:
            if i.isdigit():
                the_frequency_tx.append(i)
            else:
                pass
        num2 = ''.join(the_frequency_tx)
        command3 = "show rf rx-frequency"
        results = self.send_command(command3)
        split_string = results.split(" ")
        my_num3 = split_string[-1]
        the_frequency_rx = []
        for i in my_num3[:5]:
            if i.isdigit():
                the_frequency_rx.append(i)
            else:
                pass
        num3 = ''.join(the_frequency_rx)
        print(num, num2, num3)

    def get_shell(self):
        return self.connection

    def close(self):
        if self.client.get_transport().is_active():
            self.client.close()

    ##############################################################################

    def copy_running_startup(self):
        self.send_command("copy running-configuration startup-configuration")

    def show_sw_not_active_version(self, eth_type, value, value_prefix):
        print(f"Device details : {self.server_ip} -> set eth eth2 eth-type "
              f"{eth_type} {value}{value_prefix}")
        self.send_command(f"set eth eth2 eth-type {eth_type} {value}{value_prefix}")
    #######################################################################################

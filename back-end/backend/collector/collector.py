import telnetlib
import time
import re
import time

from .models import Management, Device, Interface


class Collector:
    def findHostname(self, hostname_data):
        # Finding hostname
        regex = re.compile('hostname \w*')
        hostname = ''.join(regex.findall(hostname_data)).split(' ')[1]

        # return hostname of current device
        return hostname

    def findNeighbors(self, cdp_data):
        # Finding DEVICE from cdp data
        regex = re.compile('Device\sID:\s\w*')
        device_lst = [x[x.find(': ')+2::] for x in regex.findall(cdp_data)]

        # return List() of all neighbors devices of currnet device
        return device_lst

    def findSelfInterface(self, cdp_data):
        # finding device's interfaces that we telneted
        regex = re.compile('.*Interface:.*,')
        self_inf_lst = [x[x.find(': ')+2::][0]+"".join(re.compile(
            "[^A-Za-z,]").findall(x[x.find(': ')+2::])) for x in regex.findall(cdp_data)]

        # return List() of all interface that is connected to other.
        return self_inf_lst

    def findNextInterface(self, cdp_data):
        # finding to the next interface (ongoing)
        regex = re.compile('Port ID \(outgoing port\):.*\n')
        next_inf_lst = [x[x.find(': ')+2::][0]+"".join(re.compile(
            "[^A-Za-z\r\n]").findall(x[x.find(': ')+2::])) for x in regex.findall(cdp_data)]

        # return a List() of next interface
        return next_inf_lst

    def findRelationInf_IP(self, ip_inf_data):
        # return a dictionary of IP and Interface (Like a Mapping)
        # split
        ip_lst = ip_inf_data[ip_inf_data.find("Protocol")+8:].split()
        self_ip_lst = []
        inf_name_lst = []

        for x in ip_lst:
            # identifying what is ip and what is the name of an interfaces.
            if "." in x:
                self_ip_lst.append(x)
            if "ethernet" in x.lower() or "serial" in x.lower():
                inf_name_lst.append(
                    x[0]+"".join(re.compile("[^A-Za-z]").findall(x)))

        # Return a Dict() of Device's Interface (Key) and IP (Value)
        return dict(zip(inf_name_lst, self_ip_lst))

    def findTypeofDevice(self, capa_data, self_inf_lst):
        # Identifying Type of Devices

        context = capa_data[capa_data.find("Port ID")+8:].split('\n')
        context2 = [i.split() for i in context]
        # for cutting unuse datas or clean data
        clean_data = [x for x in context2 if len(x) > 4]
        type_lst = []
        # Identifying what is devices and changing a word Like F0/0 to Fas0/0 to be a proper key.
        for i in range(len(self_inf_lst)):
            from_inf = self_inf_lst[i]
            if 'F' in from_inf:
                from_inf = from_inf.replace('F', 'Fas')
            if 'G' in from_inf:
                from_inf = from_inf.replace('G', 'Gig')
            if 'S' in from_inf:
                from_inf = from_inf.replace('S', 'Ser')
        # Make sure that is exacly this device by compare between type and interface
            if 'R' in clean_data[i][1:] and from_inf in "".join(clean_data[i][:-2]):
                type_lst.append('R')
            elif 'S' in clean_data[i][1:] and from_inf in "".join(clean_data[i][:-2]):
                type_lst.append('S')
        # return a list of type of device ordered by sequence (a sequence is refer from device list (same index))
        return type_lst

    def findNextInterfaceIP(self, cdp_data, type_lst):
        # \n\s\sIP address:\s\d*.\d*.\d*.\d*'
        regex = re.compile(
            'Entry\saddress\(es\): [\r\n]+\s\sIP address:\s\d*.\d*.\d*.\d*')
        ip_lst1 = [re.compile('\S\d*\.\d*\.\d*\.\d*').findall(x)[0]
                   for x in regex.findall(cdp_data)]
        num = 0
        ip_lst2 = []
        for x in type_lst:
            if x == 'R':
                ip_lst2.append(ip_lst1[num])
                num += 1
            else:
                ip_lst2.append("None")

        # print("ip_lst1", ip_lst1)
        # print("type_lst", type_lst)
        # print("ip_lst2", ip_lst2)
        return ip_lst2

    def packing(self, hostname, device_lst, self_inf_lst, type_of_device, next_inf_lst, relationinf, next_ip_lst):

        # A Last session before output data.

        # a main dictionary for sending.
        devices = [{
            "hostname": hostname,
            "device_type": "R",
            "interface": []
        }]

        for i in range(len(device_lst)):

            # first device is the current device so it need to fill every interface
            devices[0]["interface"].append({
                "port": self_inf_lst[i],
                "ip_addr": relationinf[self_inf_lst[i]],
                "n_hostname": device_lst[i],
                "n_interface": next_inf_lst[i]
            })

            # add other devices
            devices.append({
                "hostname": device_lst[i],
                "device_type": type_of_device[i],
                "interface": [
                    {
                        "port": next_inf_lst[i],
                        "ip_addr": next_ip_lst[i],
                        "n_hostname": hostname,
                        "n_interface": self_inf_lst[i]
                    }
                ]
            })

        # a Dict() of all devices (likely a JSON format)
        return devices

    def question():
        device_ip = str(input("Please fill your device IP:"))
        user = str(input("fill your username:"))
        password = str(input("fill device password:"))

        return device_ip, user, password

    def working(self, device_ip, user, password, en_pass):

        print("Connecting to ", device_ip)
        tn = telnetlib.Telnet(device_ip)

        # Enter user ID
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")

        # if it has a password then will input password
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")

        tn.read_until(b">")
        tn.write(b"enable\n")

        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        tn.read_until(b"#")
        tn.write(b"terminal length 0\n")

        # get for finding hostname
        tn.read_until(b"#")
        tn.write(b"show run | include hostname\n")
        hostname_data = tn.read_until(b"#").decode('utf-8')

        # get cdp detail
        tn.write(b"show cdp neighbors detail\n")
        cdp_data = tn.read_until(b"#").decode('utf-8')

        # get ip address of an interfaces
        tn.write(b"show ip interface brief | exclude unassign\n")
        ip_inf_data = tn.read_until(b"#").decode('utf-8')

        # get data for finding capabilty
        tn.write(b"show cdp neighbors\n")
        capa_data = tn.read_until(b"#").decode('utf-8')

        # disconnect
        print("Disconnecting from ", device_ip)
        tn.write(b"exit\n")

        return hostname_data, cdp_data, ip_inf_data, capa_data

    def main(self):
        time_init = time.time()
        all_managenents = Management.objects.all()
        for manage in all_managenents:
            device_ip = manage.ip_addr
            username = manage.username
            password = manage.password
            en_pass = manage.en_pass

            # session of collecting raw data.
            hostname_data, cdp_data, ip_inf_data, capa_data = self.working(self, 
                device_ip, username, password, en_pass)

            # Str() current device hostname
            hostname = self.findHostname(self, hostname_data)
            # List() of all name of neighbor device.
            device_lst = self.findNeighbors(self, cdp_data)
            # List() of all interface of current device that is connected to other.
            self_inf_lst = self.findSelfInterface(self, cdp_data)
            # List() of next interface
            next_inf_lst = self.findNextInterface(self, cdp_data)
            # Dict() of Device's Interface (Key) and IP (Value)
            relationinf = self.findRelationInf_IP(self, ip_inf_data)
            # List() of type of device ordered by sequence (a sequence is refer from device list (same index))
            type_of_device = self.findTypeofDevice(self, capa_data, self_inf_lst)
            # test
            next_ip_lst = self.findNextInterfaceIP(self, cdp_data, type_of_device)
            # Dict() output of this process (likely JSON)
            devices = self.packing(self, hostname, device_lst, self_inf_lst,
                              type_of_device, next_inf_lst, relationinf, next_ip_lst)

            for device in devices:
                obj, created = Device.objects.get_or_create(hostname=device['hostname'], device_type=device['device_type'])
                for intf in device['interface']:
                    i, c = Interface.objects.update_or_create(device=obj,port=intf['port'], ip_addr=intf['ip_addr'], n_hostname=intf['n_hostname'], n_interface=intf['n_interface'])
                    # print('interf d', intf['port'], intf['n_interface'])
                    # intf stand for interface (of device['interface']) | i, c for obj, created = update_or_create
            time_end = time.time()
            print('Discovery and update time :  %.4f'  %(time_end - time_init), ' seconds.')

            # print('devices', devices)
        # print("--------Welcome to Discovery--------")
        # print("Please fill all require information carefully")
        # print("Follow the insturction\n")

        # a question for asking about username and password
        # device_ip, username, password = question()

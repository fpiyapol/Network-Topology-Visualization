from .models import Device, Interface, Management


class CTest():
    """ This class for test class """
    def test():
        data_set = [{
            'interface': ['F0/0|196.0.0.1|Switch|G0/1', 'F0/1|10.0.0.1|R2|F0/1'],
            'hostname': 'iridiumR1',
            'd_type': 'R'
        }, {
            'interface': ['G0/1|???|iridiumR1|F0/0'],
            'hostname': 'Switch',
            'd_type': 'R'
        }, {
            'interface': ['F0/1|???|iridiumR1|F0/1'],
            'hostname': 'R2',
            'd_type': 'R'
        }]
        print('in test process')
        # obj, created = Device.objects.update_or_create(
        #     hostname='Router1', device_type='S', defaults={'device_type': 'R'})

        obj, created = Interface.objects.update_or_create(
            port='G0/1', ip_addr='3.3.3.3', defaults={'port': 'G0/2'}
        )
        
        # for data in data_set:
        #     # in this loop d stand for device and i stand for interface (use when create new object to database)
        #     d = Device(hostname=data['hostname'], device_type=data['d_type'])
        #     d.save()
        #     # i = Interface()
        #     for intf in data['interface']:
        #         intf = intf.split('|')
        #         print(intf)
        #         i = Interface(
        #             device=d, port=intf[0], ip_addr=intf[1], n_hostname=intf[2], n_interface=intf[3])
        #         i.save()
        # print('done')
        # try:
        #     t = Device.objects.get(hostname="Name")
        # except:
        #     print('not found')
        # print('test \t', Device.objects.filter(hostname="NameTest"))

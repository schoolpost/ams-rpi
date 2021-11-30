class AMS_Helper:
    def __init__(self):
        self.ams_mac = None
        self.ams_name = None
        self.ams_resolution = [0,0]

        CFG_FILE = '/boot/config.txt'

        with open(CFG_FILE, 'r') as config:
            for line in config.read().splitlines():
                try:
                    var, val = line.split('=')
                    if "ams_device_mac" in var:
                        self.ams_mac = val
                    if "ams_device_name" in var:
                        self.ams_name = val
                    if "ams_resolution" in var:
                        w, h = val.split("x")
                        self.ams_resolution[0] = w
                        self.ams_resolution[1] = h 

                except Exception as e:
                    pass

    def get_device(self):
        return (self.ams_mac, self.ams_name)


    def get_resolution(self):
        return (self.resolution[0], self.resolution[1])
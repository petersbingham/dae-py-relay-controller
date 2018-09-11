from pylibftdi import Driver

for dev in Driver().list_devices():
    print(dev)


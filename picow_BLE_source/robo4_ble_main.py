import bluetooth
from ble_simple_peripheral_b import BLESimplePeripheral
import machine
import robo4

def main():
    ble = bluetooth.BLE()
    p = BLESimplePeripheral(ble)

    led = machine.Pin("LED", machine.Pin.OUT)
    robo = robo4.robo4()

    def on_rx(data):
        cmd = data.decode('utf-8').replace('\n','')
        print(cmd)
        if not robo.set_request_name(cmd):
            if cmd == 'get angles_init':
                fr, hr, fl, hl = robo.get_angles_ini()
                tx_str = 'ri ' + str(fr) + ',' + str(hr) + ',' + str(fl) + ',' + str(hl)
                print(tx_str)
                p.send(tx_str)
            elif cmd == 'get angles':
                fr, hr, fl, hl = robo.get_angles()
                tx_str = 'ra ' + str(fr) + ',' + str(hr) + ',' + str(fl) + ',' + str(hl)
                print(tx_str)
                p.send(tx_str)
            else:
                para = cmd.split(' ')
                if len(para) == 2:
                    angles = para[1].split(',')
                    if para[0] == 'si':
                        robo.set_angles_ini(int(angles[0]), int(angles[1]), int(angles[2]), int(angles[3]))
                        robo.set_angle_direct(0, 0, 0, 0)
                    if para[0] == 'sa':
                        robo.set_angle_direct(int(angles[0]), int(angles[1]), int(angles[2]), int(angles[3]))

    p.on_write(on_rx)

    while True:
        if p.is_connected():
            led.on()
        else:
            led.off()

if __name__ == "__main__":
    main()

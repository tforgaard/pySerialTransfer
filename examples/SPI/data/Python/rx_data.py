from time import sleep
from pySerialTransfer import pySPITransfer as txfer

from periphery import GPIO


print("opening gpio")
gpio_data_ready_in = GPIO("/dev/gpiochip0", 7, "in", edge="rising") # pin 22


gpio_debug_pin = GPIO("/dev/gpiochip0", 38, "out") # pin 38 or 40


class struct(object):
    z = ''
    y = 0.0


arr = ''

transmit = False


if __name__ == '__main__':
    try:
        testStruct = struct
        link = txfer.SPITransfer(port='/dev/spidev0.0', spi_mode=0, baud=20000000, debug=False)
        
        link.open()
        sleep(5)
        num_rec = 0
    
        while True:

            if gpio_data_ready_in.read() and not transmit:
                transmit=True
            
            available, transmit = link.available(transmit)
            if available:
                recSize = 0
                gpio_debug_pin.write(True)
                # simple_arr = link.rxBuff[0:248]
                simple_arr = link.rx_obj(obj_type=list,start_pos=recSize,list_format='B',obj_byte_size=248)

                recSize += len(arr)
                
                print("simple arr:", simple_arr)
                sleep(0.1)
                num_rec += 1
                gpio_debug_pin.write(False)
                
            elif link.status < 0:
                if link.status == txfer.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif link.status == txfer.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif link.status == txfer.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(link.status))
            else:
                # print("sleeping")
                pass
                # sleep(0.01) # sleep 10ms
                
        
    except KeyboardInterrupt:
        link.close()

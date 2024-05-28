# Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
# Bus 001 Device 005: ID 413c:2106 Dell Computer Corp. QuietKey Keyboard
# Bus 001 Device 009: ID 0483:5840 STMicroelectronics 58Printer
# Bus 001 Device 003: ID 1ea7:0066 SHARKOON Technologies GmbH
# Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub
# Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

# lsusb -vvv -d 0483:5840 | grep iInterface
# lsusb -vvv -d 0483:5840 | grep bEndpointAddress | grep OUT
# SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5840", MODE="0664", GROUP="dialout"

# from escpos.printer import Usb
from escpos import *
vendor_id= 0x0483
product_id = 0x5840
import secrets
import string
from Crypto.Random import random

def print_receipt_func(large_bottle, small_bottle):
    try: 
        Gooj = printer.Usb(vendor_id,product_id,0, in_ep=0x81,out_ep=0x04)
        divider = "******************************"
        large_rate = 0.5
        small_rate = 0.25
        col3 = "{:<15} {:>4} {:>8}"
        Gooj.set(align='center')
        Gooj.image("./images/cen1.png")
        Gooj.ln(3)
        Gooj.set(font='a', width=1, bold=True)
        Gooj.textln(col3.format("Bottle Type", "Qty", "Points") + '\n')
        Gooj.set_with_default()
        Gooj.set(align='center', font='a', width=1, height=6)
        large_points = large_rate*large_bottle
        small_points = small_rate*small_bottle
        Gooj.textln(col3.format("Large Bottle", f"{large_bottle}", f"{large_points}"))
        Gooj.textln(col3.format("Small Bottle", f"{small_bottle}", f"{small_points}"))
        Gooj.textln(divider)
        Gooj.set_with_default()
        Gooj.set(align='center', font='a', bold=True, width=6)
        print(large_points + small_points)
        Gooj.textln(f"Total Points: {((large_points + small_points))}")
        Gooj.textln(f"Total Price: {((large_points + small_points)*3)}")
        Gooj.textln(divider)
        Gooj.ln()
        alphabet = string.ascii_letters + string.digits
        orderId = ''.join(random.sample(alphabet, 30))
        Gooj.qr(orderId, size=12, center=True)

        # Cut paper
        Gooj.cut()
    except Exception as e:
        print(f"Error: {e}")



# print_receipt_func(3,3)
#!/usr/bin/python3.5
import time
import datetime
from utils import *
import pyzk.pyzk as pyzk
import pyzk.zkmodules.defs as defs

"""
Test script to test/show several functions of the terminal spec/lib.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

time.sleep(0)  # sometimes a delay is useful to se

ip_address = '103.205.71.124'  # set the ip address of the device to test
machine_port = 4370

z = pyzk.ZKSS()

print_header("TEST OF TERMINAL FUNCTIONS")

# connection
print_header("1.Connection Test")
print_info("First, connect to the device and then disable the device")
z.connect_net(ip_address, machine_port)
z.disable_device()




# get more params
print_header("4.Device info test")

print_info("Some parameter requests:")

print('Vendor = ' + z.get_vendor())
print('Product code = |{0}|'.format(z.get_product_code()))
print('Product time = |{0}|'.format(z.get_product_time()))
print('card function = |{0}|'.format(z.get_cardfun()))
print('User max id width = |{0}|'.format(z.get_device_info('~PIN2Width')))
print('Firmware version = |{0}|'.format(z.get_firmware_version()))


# get state
print_header("5.Get device state")
print('Device state = |{0}|'.format(z.get_device_state()))

# finally enable the device and terminate the connection
z.enable_device()
z.disconnect()


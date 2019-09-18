#!/usr/bin/python3.5
import time
import os.path
from utils import *
import pyzk.pyzk as pyzk
from pyzk.zkmodules.defs import *

"""
Test script to test/show several functions of the access spec/lib.

The script test_other.py should be executed before this script, so the
fp templates fp1 and fp2 are available.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

time.sleep(0)

ip_address = '103.91.229.62'  # set the ip address of the device to test
machine_port = 4370

print_header("TEST OF ACCESS FUNCTIONS")

z = pyzk.ZKSS()
z.connect_net(ip_address, machine_port)
z.disable_device()

print_header("1.Read all user info")


print_header("")
z.read_all_user_id()
# z.read_all_fptmp()
z.print_users_summary()

z.enable_device()
z.disconnect()

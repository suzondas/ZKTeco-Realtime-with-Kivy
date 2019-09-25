'''
Realtime Monitoring of Zkteco Fingerprint Machines. It receive event from machine and fetch event wise user data
from database and then show the amalgamated information in GUI Screen. N.B. This is not under any GPL.
ALl rights reserved by Suzon Das [https://www.github.com/suzon-das]
'''
from kivy import Config

Config.set('graphics', 'multisamples', '0')
# Python Libraries
import webbrowser
from os.path import dirname, join
from threading import Thread
from time import time, sleep
from urllib.request import urlopen
import winsound
import pyttsx3 as pyttsx3
import json
from kivy.core.window import Window

from kivy.uix.scrollview import ScrollView

from utils import *

# Kivy libraries [https://kivy.org/]
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, \
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from functools import partial

# ZKTeco Python Libraries [https://github.com/fananimi/pyzk]. Kudos to Fanani M. Ihsan
import pyzk.pyzk as pyzk
from pyzk.zkmodules.defs import *
from pyzk.misc import *
from kivy.core.audio import SoundLoader

engine = pyttsx3.init()

rate = engine.getProperty('rate')
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

# Use female English voice
engine.setProperty('voice', en_voice_id)
engine.setProperty('rate', 180)
engine.say('Welcome to Fitness plus BD')
engine.runAndWait()
# Zkteco libraries initializing
ip_address = '103.91.229.62'  # set the ip address of the device to test
machine_port = 4370

z = pyzk.ZKSS()

# connection
z.connect_net(ip_address, machine_port)
# read user ids
z.disable_device()
z.read_all_user_id()
z.enable_device()

# enable the report of rt packets
z.enable_realtime()

# Initializing global variables
evntMsg = ''  # event wise message
arr = [100388,555, 100291, 100482 ]
arrs = ['04:22','04:32', '04:45', '04:53' ]
flag =0

# functions to produce record with null value
def noResponseRecord():
    layout.add_widget(Label(text="--", size_hint_x=None, width=250, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(Label(text="--", size_hint_x=None, width=50, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(Label(text="--", size_hint_x=None, width=100, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(Label(text="--", size_hint_x=None, width=100, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(Label(text="--", size_hint_x=None, width=150, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(Label(text="--", size_hint_x=None, width=50, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(Label(text="--", size_hint_x=None, width=150, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(Label(text="--", size_hint_x=None, width=100, color=(1.0, 0.0, 0.0, 1.0)))
    layout.add_widget(
        Button(text='No Link', size_hint_x=None, width=80, background_color=(1.0, 0.0, 0.0, 1.0)))


# Listen Event and then Fetch data if member successfully verified and then fetch details of that user based on
# member id returned from machine and then adding those data to layout row
def eventThread():
    # wait for event
    # z.recv_event()
    # ev = z.get_last_event()
    ev = EF_ATTLOG

    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)  # beep when event triggered in machine
    global evntMsg
    evntMsg = "New Event Found"

    # process the event
    if ev == EF_ALARM:
        evntMsg = 'Alarm Event'

    # Our main area. It is true when member successfully verified by ZKTeco
    elif ev == EF_ATTLOG:
        evntMsg = 'User Accessed'
        # t = tuple(z.parse_event_attlog())
        # userId = t[0]  # Member Id set on machine
        global flag
        userId = arr[flag]  # Member Id set on machine
        # userTime = t[2]  # Time of access
        userTime = arrs[flag]  # Time of access

        if userId == 555:
            engine.say('Admin Finger')
            engine.runAndWait()

        from urllib.request import Request, urlopen

        req = Request(
            'http://door.fitnessplusbd.com/uttara/users/userSubscription?id=' + str(userId),
            headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        data = json.loads(webpage)

        if data["stat"] == 200:
            engine.say('Hi ' + str(data["name"]) + ', Thank you')
            engine.runAndWait()
            layout.add_widget(Label(text=str(data["name"]), size_hint_x=None, width=250, color=(1.0, 1.0, 0.0, 1.0)))
            layout.add_widget(Label(text=str(data["id"]), size_hint_x=None, width=50))
            layout.add_widget(Label(text=str(data['membership_valid_from']), size_hint_x=None, width=100))
            layout.add_widget(Label(text=str(data['membership_valid_to']), size_hint_x=None, width=100))
            layout.add_widget(Label(text=str(data['category']), size_hint_x=None, width=150))
            layout.add_widget(Label(text=str(data['branch']), size_hint_x=None, width=50))
            layout.add_widget(Label(text=str(userTime), size_hint_x=None, width=150))

            if str(data['status']) == 'Not Paid':
                engine.say('Not Paid')
                engine.runAndWait()
                layout.add_widget(
                    Label(text=str(data['status']), size_hint_x=None, width=100, color=(1.0, 0.0, 1.0, 1.0),
                          bold=True, ))
            else:
                layout.add_widget(Label(text=str(data['status']), size_hint_x=None, width=100))

            layout.add_widget(Button(text='Details', size_hint_x=None, width=80, on_press=partial(webbrowser.open,
                                                                                                  'http://door.fitnessplusbd.com/uttara/users/redirectFromKivy?id=' + str(
                                                                                                      data["id"]))))

            d1 = datetime.datetime.strptime(str(data['membership_valid_to']), "%d/%m/%Y").strftime("%Y-%m-%d")
            d2 = str(datetime.datetime.now())

            if d2 > d1:
                engine.say('Membership Expired')
                engine.runAndWait()
        else:
            engine.say('Admin Finger')
            engine.runAndWait()
    elif ev == EF_FINGER:
        evntMsg = 'Someone placed Finger'
    elif ev == EF_ENROLLUSER:
        evntMsg = "EF_ENROLLUSER: Enrolled user"
    elif ev == EF_ENROLLFINGER:
        evntMsg = "EF_ENROLLFINGER: Enroll finger finished"
    elif ev == EF_BUTTON:
        evntMsg = "EF_BUTTON: Pressed button"
    elif ev == EF_UNLOCK:
        evntMsg = "EF_UNLOCK: Unlock event"
    elif ev == EF_VERIFY:
        user_sn = z.parse_verify_event()
        if user_sn == 0xffffffff:
            evntMsg = "Wrong Fingerprint Entered"
        else:
            evntMsg = "New Fingerprint Entered"
    elif ev == EF_FPFTR:
        evntMsg = "EF_FPFTR:"
    else:
        evntMsg = "Unknown Event"
        noResponseRecord()

    # Callback to own so that the listening event continues after one event
    flag = flag +1
    sleep(15)
    eventThread()


# Calling the Event Listener function using thread
def listenEvent():
    t = Thread(target=eventThread)
    t.daemon = True
    t.start()


# Main Layout. Here 8 columns for showing details of accessed users
layout = GridLayout(cols=9, spacing=10, size_hint_y=None, row_force_default=True, row_default_height=40)
layout.bind(minimum_height=layout.setter('height'))
layout.add_widget(
    Label(text='Name', size_hint_x=None, width=250, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True, font_size='16dp',
          underline=True))
layout.add_widget(
    Label(text='ID No', size_hint_x=None, width=50, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True, font_size='16dp',
          underline=True))
layout.add_widget(
    Label(text='Starting Date', size_hint_x=None, width=100, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True,
          font_size='16dp', underline=True))
layout.add_widget(Label(text='End Date', size_hint_x=None, width=100, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True,
                        font_size='16dp', underline=True))
layout.add_widget(Label(text='Category', size_hint_x=None, width=150, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True,
                        font_size='16dp', underline=True))
layout.add_widget(
    Label(text='Branch', size_hint_x=None, width=50, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True, font_size='16dp',
          underline=True))
layout.add_widget(
    Label(text='Time', size_hint_x=None, width=150, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True, font_size='16dp',
          underline=True))
layout.add_widget(
    Label(text='Payment Status', size_hint_x=None, width=100, height=40, color=(1.0, 0.0, 1.0, 1.0), bold=True,
          font_size='16dp', underline=True))
layout.add_widget(
    Label(text='Action', size_hint_x=None, width=80, height=30, color=(1.0, 0.0, 1.0, 1.0), bold=True, font_size='16dp',
          underline=True))
root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), bar_width=4)  # !important
root.add_widget(layout)


class RealTime(App):
    def build(self):
        listenEvent()
        return root


# Window.fullscreen = True
Window.clearcolor = (0.106, 0.282, 0.435, 1)
RealTime().run()

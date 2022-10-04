#!/usr/bin/python
# SPDX-License-Identifier: LGPL-2.1-or-later


import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import configparser
import time
#from kosha_central import get_services_and_characs
from lib.my_logging import log_msg

import lib.bluetooth_utils as UTILS
import lib.bluetooth_constants as CONST
import sys, signal
import platform


# GLOBALS
VERSION = 'Peripheral Device Tester V0.4 4/Oct/2022'
config = configparser.ConfigParser()
connected = False
services_resolved = False
log_level="INFO"
wdt_timeout = 10
addrs = []
relevant_ifaces = ( CONST.ADAPTER_INTERFACE, CONST.DEVICE_INTERFACE )

##
log_msg.info(VERSION)
log_msg.info(f"Platform: {platform.platform()}")
log_msg.info(f"Python: {sys.version}")

try:
    config.read("config.yaml")
    addrs = UTILS.parse_mac_addr(config['DEVICES']["ble1"])
    log_level = config['SYSTEM']['log_level']
    log_detail = int(config['SYSTEM']['detail'])
    wdt_timeout = int(config['SYSTEM']['wdt_timeout'])
    log_added = int(config['SYSTEM']['log_added'])
    log_removed = int(config['SYSTEM']['log_removed'])
    WDT_delay = int(config['SYSTEM']['wdt_delay']) 
    disconnect_delay = int(config['SYSTEM']['disconnect_delay'])
    show_skipped_packets = int(config['SYSTEM']['show_skipped_packets'])
    not_of_interest = int(config['SYSTEM']['not_of_interest'])
    
    force_connect = int(config['DEVICES']['force_connect'])

    log_msg.info (f"CONFIG: wdt_timeout = {wdt_timeout}")
    log_msg.info (f"CONFIG: log_level = {log_level}")
    log_msg.info (f"CONFIG: Looking for : {addrs}")
    log_msg.info (f"CONFIG: log key/value = {log_detail}")
    log_msg.info (f"CONFIG: log added devices = {log_added}")
    log_msg.info (f"CONFIG: log removed devices = {log_removed}")
    log_msg.info (f"CONFIG: force connect {force_connect}")

    addrs = [x.replace(":","_") for x in addrs ]
except Exception as e:
    print(e)

def property_changed(interface, changed, invalidated, path):
    global devices, current_path
    iface = interface[interface.rfind(".") + 1:]
    #print(f"[{interface}]")
    if "Device1" in interface:
        # check if it is device of interest - get "_" separated mac address from path
        _devaddr = path[path.rfind("/")+5:]
        if _devaddr in addrs:
            pkeyval(changed,f"CHG: {_devaddr} ")
        else:
            if not_of_interest:
                log_msg.info(f"CHG: Device Not of interest : {_devaddr}")
    else:
        if not_of_interest:
            log_msg.info(f"CHG: Interface not of interest: {iface}")

def interfaces_added(path, interfaces):
    for iface, props in interfaces.items():
        if not(iface in relevant_ifaces) or log_added == 0:
            continue
        if iface in CONST.ADAPTER_INTERFACE:
            log_msg.info(f"ADD: Adapter [{path}]")
        else:
            # its a device interface : get name and address from props and path respectively
            _devaddr = path[path.rfind("/")+5:]
            _name = "None"
            if "Name" in props.keys():
                _name = props['Name']
            log_msg.info(f"ADD: Device {_devaddr} Name: {_name}" )

def interfaces_removed(path, interfaces):
    for iface in interfaces:
        if not(iface in relevant_ifaces) or log_removed == 0:
            continue
        if iface in CONST.DEVICE_INTERFACE:
            _devaddr = path[path.rfind("/")+5:]
            log_msg.info(f"DEL: Device {_devaddr}")

def pkeyval(d,title=None):
    ''' given d dbus dict print key val : Warning no checking for types'''
    for k,v in d.items():
        log_msg.info(f"{title} {UTILS.dbus_to_python(k)} = {UTILS.dbus_to_python(v)}")
    
### I KNOW THIS NAME CLASHES WITH ONE IN
### UTILS but for now leave it as is
def find_adapter():
    objects=UTILS.get_managed_objects()
    for o, props in objects.items():
        if CONST.GATT_MANAGER_INTERFACE in props.keys():
            return o

def signal_handler(sig, frame):
    #global buff, fname
    global devices
    try:
        mainloop.quit()
    except Exception as e:
        log_msg.error(e)    
    log_msg.info("Exiting")
    sys.exit(0)


if __name__ == '__main__':
    
    global bus
   
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    bus.add_signal_receiver(property_changed, bus_name="org.bluez",
            dbus_interface="org.freedesktop.DBus.Properties",
            signal_name="PropertiesChanged",
            path_keyword="path")
    
    bus.add_signal_receiver(interfaces_added, bus_name="org.bluez",
            dbus_interface="org.freedesktop.DBus.ObjectManager",
            signal_name="InterfacesAdded")

    bus.add_signal_receiver(interfaces_removed, bus_name="org.bluez",
            dbus_interface="org.freedesktop.DBus.ObjectManager",
            signal_name="InterfacesRemoved")
    
    
    ## set up control-c handler
    signal.signal(signal.SIGINT, signal_handler)
    
    mainloop = GLib.MainLoop()
    #mainloop = GObject.MainLoop()

    ## get adapter
    adapter = UTILS.find_adapter()
    try:
        ## start discovery
        adapter.StartDiscovery()
    except Exception as e:
        log_msg.error(e)
        sys.exit(1)

    mainloop.run()
    
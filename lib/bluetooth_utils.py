#!/usr/bin/python3
import dbus
import sys, re
import configparser


from sys import stdin, stdout
sys.path.insert(0, '.')
from .bluetooth_constants import *

def byteArrayToHexString(bytes):
    hex_string = ""
    for byte in bytes:
        hex_byte = '%02X' % byte
        hex_string = hex_string + hex_byte
    return hex_string

def convert_to_hex(row):
    ''' give a array of integers each less than 255 - convert to hex string '''
    
    if isinstance(row,list):
        hex_string = ''
        for i in row:
            hex_string = hex_string + f"{i:02X}"
    return hex_string

def buffer_to_file(buff,fname):
    ''' write buffer to file : file is overwritten '''
    with open(fname,"w") as f:
        for row in buff:
            f.write(convert_to_hex(row)+'\n')   

def get_managed_objects():
	bus = dbus.SystemBus()
	manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, "/"),DBUS_OM_IFACE)
	return manager.GetManagedObjects()


def find_adapter(pattern=None):
	return find_adapter_in_objects(get_managed_objects(), pattern)

def find_adapter_in_objects(objects, pattern=None):
	bus = dbus.SystemBus()
	for path, ifaces in objects.items():
		adapter = ifaces.get(ADAPTER_INTERFACE)
		if adapter is None:
			continue
		if not pattern or pattern == adapter["Address"] or \
							path.endswith(pattern):
			obj = bus.get_object(BLUEZ_SERVICE_NAME, path)
			return dbus.Interface(obj, ADAPTER_INTERFACE)
	raise Exception("Bluetooth adapter not found")



def dbus_to_python(data):
    if isinstance(data, dbus.String):
        data = str(data)
    if isinstance(data, dbus.ObjectPath):
        data = str(data)
    elif isinstance(data, dbus.Boolean):
        data = bool(data)
    elif isinstance(data, dbus.Int64):
        data = int(data)
    elif isinstance(data, dbus.Int32):
        data = int(data)
    elif isinstance(data, dbus.Int16):
        data = int(data)
    elif isinstance(data, dbus.UInt16):
        data = int(data)
    elif isinstance(data, dbus.Byte):
        data = int(data)
    elif isinstance(data, dbus.Double):
        data = float(data)
    elif isinstance(data, dbus.Array):
        data = [dbus_to_python(value) for value in data]
    elif isinstance(data, dbus.Dictionary):
        new_data = dict()
        new_key = ""
        for key in data.keys():
            new_key = dbus_to_python(key)
            new_data[new_key] = dbus_to_python(data[key])
        data = new_data
    return data

def device_address_to_path(bdaddr, adapter_path):
    # e.g.convert 12:34:44:00:66:D5 on adapter hci0 to /org/bluez/hci0/dev_12_34_44_00_66_D5
    path = adapter_path + "/dev_" + bdaddr.replace(":","_")
    return path




def get_name_from_uuid(uuid):
    if uuid in bluetooth_constants.UUID_NAMES:
        return bluetooth_constants.UUID_NAMES[uuid]
    else:
        return "Unknown"

def text_to_ascii_array(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))
    return ascii_values

def print_properties(props):
    # dbus.Dictionary({dbus.String('SupportedInstances'): dbus.Byte(4, variant_level=1), dbus.String('ActiveInstances'): dbus.Byte(1, variant_level=1)}, signature=dbus.Signature('sv'))
    for key in props:
        print(key+"="+str(props[key]))


def get_objects_and_props(bus,**kwargs):
    '''
    get_object_and_props returns a dict of bluez objects, properties with object path as key

    Arguments:
    bus : the connection object to bluez

    keyword args:
    filter : filter for returning dict.

    '''
    ret_val={}
    INTERFACES = [bluetooth_constants.DEVICE_INTERFACE, 
                    bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE, 
                    bluetooth_constants.GATT_SERVICE_INTERFACE]

    proxy_object = bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME,'/')
    manager = dbus.Interface(proxy_object,bluetooth_constants.DBUS_OM_IFACE)
    objects = manager.GetManagedObjects()
    filter=kwargs.get("filter","")
    print(f"filter : {filter}")
    for path, interfaces in objects.items():
        if filter not in path:
            continue
        #print("processing ",path)
        proxy_object = bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME,str(path))
        for interface in interfaces.keys():
            if interface  in INTERFACES:

                try:
                    iface = str(interface)
                    props = proxy_object.GetAll(iface,dbus_interface=bluetooth_constants.DBUS_OM_PROPERTIES)
                    ret_val[path]=(proxy_object,props)
                except Exception as e:
                    pass
    return ret_val

### Config related routines
def readtill(char,str):
    # reads str till char returns str1,str2
    # str1 is string before char
    # str2 is string after char
    
    # avoids deadlock
    if str[0]==char:
        str=str[1:]
    for i in range(len(str)):
        if str[i] == char:
            return str[:i],str[i+1:]
    return None,str 

def parse_mac_addr(blestring):
    # given a string of addresses each of which is enclosed in sinle quotes
    # returns arrage of strings (mac addresses)
    SEP = "'"
    COLON = ":"
    addr = []
    substr, str = readtill(SEP,blestring)
    while COLON in str :
        #print(f"substr: {substr} str: {str}")
        if COLON in substr and len(substr) == 17:
            addr.append(substr)
            #print(f"addr : {addr}")
        substr,str = readtill(SEP,str)
        #print(f"\tsubstr: {substr} str: {str}")
    # corner case 
    if (not substr == None) and (COLON in substr) and len(substr) == 17:
        addr.append(substr)    
    return addr


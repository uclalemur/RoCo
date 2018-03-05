from roco.api.component import Component
from roco.library import *
from roco.library import get_component

if __name__ == "__main__":
    c = Component(name = 'ArduinoCode')
    c.add_subcomponent('serial_in0', 'serial_in')
    c.add_subcomponent('serial_to_string0', 'serial_to_string')
    c.add_subcomponent('string_compare0', 'string_compare')
    c.add_connection(('', 'ial_in0->received'), ('serial_to_string0', 'received'))
    c.add_connection(('', 'ial_in0->came'), ('serial_to_string0', 'came'))
    c.add_connection(('', 'ial_to_string0->cameOut'), ('string_compare0', 'inDetected'))
    c.add_connection(('', 'ial_to_string0->receivedString'), ('string_compare0', 'inString'))
    c.to_yaml("library/ArduinoCode.yaml")

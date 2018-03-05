from roco.api.component import Component
from roco.library import *
from roco.library import get_component

if __name__ == "__main__":
    c = Component(name = 'DrivenServo')
    c.add_subcomponent('servo0', 'servo')
    c.add_subcomponent('servo_driver0', 'servo_driver')
    c.add_connection(('servo_driver0', 'eOut'), ('servo0', 'eIn'))
    c.inherit_interface('PWMin', ('servo_driver0', 'PWMin'))
    c.inherit_interface('inInt', ('servo_driver0', 'inInt'))
    c.to_yaml("library/DrivenServo.yaml")

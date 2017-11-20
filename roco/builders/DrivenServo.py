from roco.api.component import Component
from roco.library import *
from roco.library import get_component

c = Component(name = 'DrivenServo')
c.add_subcomponent('driver', 'servo_driver')
c.add_subcomponent('servo', 'servo')
c.add_connection(('driver', 'eOut'), ('servo', 'eIn'))
c.inherit_interface('PWMin', ('driver', 'PWMin'))
c.to_yaml("library/DrivenServo.yaml")

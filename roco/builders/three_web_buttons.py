from roco.api.component import Component
from roco.library import *
from roco.library import get_component

c = Component(name = 'interface')
c.add_subcomponent('button_one', 'web_button')
c.add_subcomponent('button_two', 'web_button')
c.add_subcomponent('button_three', 'web_button')
c.get_subcomponent('button_one').set_parameter('buttonValue', 'GO')
c.get_subcomponent('button_two').set_parameter('buttonValue', 'BACK')
c.get_subcomponent('button_three').set_parameter('buttonValue', 'STOP')
c.make_output()
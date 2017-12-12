from roco.api.component import Component
rWithTab = Component()
rWithTab.add_subcomponent('r1','Square')
rWithTab.add_subcomponent('r2','Square')
rWithTab.add_subcomponent('r3','Square')
rWithTab.add_connection(('r1','r'),('r2','l'), angle=120) ## this goes with 3D geometry instead of 2D pattern. ##
rWithTab.add_connection(('r2','r'),('r3','l'), angle=120)
rWithTab.add_connection(('r3','r'),('r1','l'), angle=120, tab=True) ## you also add tab besides connection. ##
rWithTab.make_output()



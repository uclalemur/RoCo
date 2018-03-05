██████╗  ██████╗  ██████╗ ██████╗ 
██╔══██╗██╔═══██╗██╔════╝██╔═══██╗
██████╔╝██║   ██║██║     ██║   ██║
██╔══██╗██║   ██║██║     ██║   ██║
██║  ██║╚██████╔╝╚██████╗╚██████╔╝
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝                                   

By UCLA LEMUR

Enables the rapid design and implementation of robots.

**PLEASE ADHERE TO STYLE GUIDE WHEN EDITING/COMMITING CODE:
https://google.github.io/styleguide/pyguide.html
**

Documentation of Roco is in ./doc/build/html/index.html

Installation
------------
1. Clone this repository: 'git clone git@git.uclalemur.com:RobotCompiler/roco.git'
2. Install dependencies: 'pip install -r requirements.txt'
3. Add this directory to path: 'export PYTHONPATH=$PYTHONPATH:/path/to/this/dir'
4. Verify installation: 'python roco/tests/test_parameterized.py'

If all of the tests pass, then the installation is complete!

Now you are ready to use the roco library!

Getting Started
---------------
Once you have gone through the installation, you can start using roco to build robots.

The main entities in roco are Components. Components are either base-level that are specified
in python code or they're created by a collection of Components known as sub-Components.

Base-level components are stored in the library as .py files while composite Components are
stored as .yaml files. Make sure to look at some .py and .yaml files in 'roco/library' to get
a better idea.

Components have Parameters, sub-Components, Interfaces, Connections and Composables.

Parameters: values that specify the form/function of the Component. For example,
a Rectangle Component will have length and width parameters. These parameters can
be variables that are solved for or constants.

Composables: instructions to generate physical output. There can be multiple type of composables
such as a graph that generates mechanical output, code that generates software output and
electrical that outputs wiring instructions. For example, a Rectangle will have a graph composable
with a Rectangular face.

Ports: these are Composable-level distinctions that specify that another Composable can be attached
to it.

Interfaces: named sets of Ports that can be connected to. Interfaces are a Component-level
abstraction of Ports.

Connections: A list of interface to interface connections of the Component's sub-Components.
These also may include a list of connection arguments. 

Base-level Components do not have sub-Components and the Composables are constructed by the
creator in python code. Since they do not have sub-Components, they do not have Connections either.

The code below shows how to create an extremeley simple 90-degree fold component.

from roco.api.component import Component
c = Component()
c.add_subcomponent("r1","Rectangle")
c.add_subcomponent("r2","Rectangle")
c.add_connection(("r1","r"),("r2","l),angle=90)
c.make_output()

Happy roboting!

Updating documentation
----------------------
1. Run the following command: cd doc
2. Run the following command: ./update_doc.py -f -d ./source/ -s rst -n ROCO -m 3 ../roco/
3. Then run: make html
4. To see a list of options supported by update_doc.py, run: ./update_doc.py -h

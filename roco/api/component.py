"""Component class and helper function.

This module contains the Component class, as well as a helper function to load
components.

"""

from collections import OrderedDict
from os.path import join
import sys

import yaml
import copy
import roco.utils.mymath as math
from roco.api.utils.variable import Variable

from roco import ROCO_DIR
from roco.utils.utils import prefix as prefix_string
from roco.utils.utils import try_import
from roco.utils.io import load_yaml
from sympy import Symbol, Eq, StrictGreaterThan, GreaterThan, StrictLessThan, LessThan
from port import Port
from interface import Interface
from connection import Connection
from parameterized import Parameterized

def get_subcomponent_object(component, name=None, **kwargs):
    """Function to generate an instantiated component from the class name.

    Args:
        component (str): The name of the component class to instantiate.
        name (:obj:`str`, optional): The name to set for the component.
        **kwargs: Arbitrary keyword arguments to pass into the constructor.

    Returns:
        The instantiated component.

    """
    try:
        obj = try_import(component, component)
        c = obj(**kwargs)
        c.setName(name)
        return c
    except ImportError:
        c = Component(component, **kwargs)
        c.setName(name)
        return c


class Component(Parameterized):
    """The base class that all components derive from.

    A component is an abstract representation of an element of a device.

    Attributes:
        subcomponents (dict): dictionary of component objects that make up the
            overall component where the key is the name.
        connections (list): list of connection definitions from an interface
            to another interface with arguments associated.
        interfaces (dict): dictionary of interfaces where the key is the name
        composables (OrderedDict): an ordered dictionary of composables that
            define the output of the component.

    """

    def __init__(self, yaml_file=None, **kwargs):
        """Constructs a new Component object.

        Creates a Component that is either blank or loaded from a yaml file.

        Args:
            yaml_file (str): The optional yaml file to load the component information from.
            **kwargs: Arbitrary keyword arguments to control construction.

        """
        Parameterized.__init__(self)

        self.subcomponents = {}
        self.connections = {}
        self.tabs = []
        self.interfaces = {}
        self._prefixed = {}
        self.composables = OrderedDict()

        if yaml_file:
            self._from_yaml(yaml_file)

        # Override to define actual component
        self.define(**kwargs)

        self.make()


    def _make_test(self, protobuf=False, display=True):
        """Constructs a test version of the Component.

        Sets test parameters as defined by the Component and creates output.

        Args:
            protobuf (Boolean): Whether to construct a protobuf or not.
            display (Boolean): Whether to display the output or not.

        """
        if not hasattr(self, '_test_params'):
            raise NotImplementedError

        for key, val in self._test_params.iteritems():
            self.set_parameter(key, val)

        name = self.__class__.__name__
        self.make_output('output/%s' % name,
                        protobuf=protobuf,
                        display=display)

    def _str_to_sympy(self, string):
        """Converts string to sympy expression

        Uses this Component's parameters to convert a string to a sympy expression.

        Args:
            string (str): The string to convert

        Returns:
            The sympy expression.

        """
        expr = math.sympify(string)
        subs = []
        for a in expr.atoms(math.Symbol):
          subs.append((a, self.get_parameter(repr(a))))
        expr = expr.subs(subs)
        return expr

    def _from_yaml(self, file_name):
        """Loads in component information from a YAML file.

        Args:
            file_name (str): The name of the yaml file.

        """
        definition = load_yaml(filename)

        # keys are (parameters, constants, subcomponents, constraints, connections, interfaces)
        try:
          for name, default in definition["parameters"].iteritems():
            self.add_parameter(name, default)
        except AttributeError: pass

        try:
          for name, default in definition["constants"].iteritems():
            self.add_constant(name, default)
        except AttributeError: pass

        try:
          for name, value in definition["subcomponents"].iteritems():
            try: 
              # XXX Can these be sympy functions as well?
              kwargs = value["constants"]
            except AttributeError:
              kwargs = {}
            self.add_subcomponent(name, value["class"], **kwargs)
            try:
              for param, pvalue in value["parameters"].iteritems():
                self.set_subcomponent_parameter((name, param), self._str_to_sympy(pvalue))
            except AttributeError:
              pass
        except AttributeError: pass

        try:
          for value in definition["constraints"]:
            self.add_constraint(self._str_to_sympy(value))
        except AttributeError: pass

        try:
          for from_port, to_port, kwargs in definition["connections"]:
            for param, pvalue in kwargs.iteritems():
                kwargs[param] = self._str_to_sympy(pvalue)
            self.add_connection(from_port, to_port, **kwargs)
        except AttributeError: pass

        try:
          for name, value in definition["interfaces"].iteritems():
            self.inherit_interface(name, (value["subcomponent"], value["interface"]))
        except AttributeError: pass
        
    def define(self, **kwargs):
        """Function for overriding interfaces.

        Args:
            **kwargs: Arbitrary keyword arguments

        """
        pass

    def add_subcomponent(self, name, object_type, **kwargs):
        """Adds a subcomponent to this Component.

        Args:
            name (str): unique identifier to refer to this subcomponent by
            object_type (str or type): code name of the subcomponent should be python file/class or yaml name

        """
        if name in self.subcomponents:
            raise ValueError("Subcomponent with name {} already exists".format(name))
        sc = {"class": obj, "parameters": {}, "constants": kwargs, "component": None}
        self.subcomponents.setdefault(name, sc)
        self.resolve_subcomponent(name)

    def del_subcomponent(self, name):
        """Deletes a subcomponent to this Component and performs any cleanup necessary

        Args:
            name (str): unique identifier of subcomponent to delete

        """
        to_delete = []

        # delete edges connecting components
        for (key, (from_comp, _), (to_comp, _), _) in self.connections:
            if name in (from_comp, to_comp):
                to_delete.append(key)
        for key in reversed(to_delete):
            self.connections.pop(key)
        if self.subcomponents[name]['component'] and 'graph' in self.subcomponents[name]['component'].composables:
            self.subcomponents[name]['component'].composables['graph'].split_merged_edges()
        self.subcomponents.pop(name)
        del self.composables['graph']
        if name in self._prefixed:
            del self._prefixed[name]
        for sc in self.subcomponents:
            if 'graph' in self.subcomponents[sc]['component'].composables:
                self.subcomponents[sc]['component'].composables['graph'].placed = False


    def add_interface(self, name, ports):
        """Adds an interface to this component.

        Args:
            name (str): unique identifier for interface that will be added to the component.
            ports (Port or list of Ports): the value that the new interface takes on.
        """
        if name in self.interfaces:
            raise ValueError("Interface %s already exists" % name)
        new_interface = Interface(name, ports)
        self.interfaces.setdefault(name, new_interface)
        return self
    
    def del_interface(self, name):
        """Deletes an interface from this component.

        Args:
            name (str): unique identifier for interface that will be deleted from the component.
        """
        self.interfaces.pop(name)
        
    def inherit_all_interfaces(self, subcomponent, prefix=""):
        """Adds all interfaces from subcomponent to current component

        Args:
            subcomponent (Component): Component object from which all the interfaces will be inherited.
            prefix (str): name of component, will automatically work if ignored or left as "" (an empty string).
        """
        self.resolve_subcomponent(subcomponent)
        obj = self.get_subcomponent(subcomponent)
        if prefix == "":
          prefix = name
        for name, value in obj.interfaces.iteritems():
          if name in self.interfaces:
            raise ValueError("Interface %s already exists" % name)
          new_interface = Interface(prefix_string(prefix, name), value)
          self.add_interface(prefix_string(prefix, name), new_interface)
        return self
    
    def inherit_interface(self, name, (subcomponent, subname)):
        """Adds specified interface from subcomponent to current component

        Args:
            name (str): New unique identifier for the interface that will be inherited.
            (subcomponent, subname) (tuple(Component, str)): Component object from which the specified interface
                will be inherited, and the name of the interface that is to be inherited from the subcomponent
        """
        if name in self.interfaces:
            raise ValueError("Interface %s already exists" % name)
        self.interfaces.setdefault(name, self.get_subcomponent_interface(subcomponent,subname))
        return self
    
    def add_connection(self, from_interface, to_interface, **kwargs):
        """ Specifies interfaces on subcomponents to be connected

        Args:
            from_interface (tuple(str, str)): a tuple containing the name of the subcomponent, and the name of the interface the connection comes from
            to_interface (tuple(str, str)): a tuple containing the name of the subcomponent, and the name of the interface the connection goes to
            kwargs (dict): arguments for the connection

        Raises:
            KeyError: a connection between the two interfaces already exists

        """
        name = "{} -> {}".format(prefix_string(from_interface[0], from_interface[1]), prefix_string(to_interface[0], to_interface[1]))
        if name in self.connections:
            raise KeyError("Connection {} already exists")
        self.connections[name] = [from_interface, to_interface, kwargs]

    def del_connection(self, from_interface, to_interface):
        """ Deletes the connection that consists of the two ordered interfaces

        Args:
            from_interface (tuple(str, str)): a tuple containing the name of the subcomponent, and the name of the interface the connection comes from
            to_interface (tuple(str, str)): a tuple containing the name of the subcomponent, and the name of the interface the connection goes to

        Raises:
            KeyError: a connection between the two interface does not exist

        """
        name = "{} -> {}".format(prefix_string(from_interface[0], from_interface[1]), prefix_string(to_interface[0], to_interface[1]))
        if name not in self.connections:
            raise KeyError("Connection {} does not exist")
        
    def to_yaml(self, filename):
        """ Generates YAML file containing component information

        Args:
            filename (str): name of the yaml file to be generated
        """
        parameters = {}
        constants = {}
        for k, v in self.parameters.iteritems():
            if isinstance(v, Variable):
              parameters[k] = v.get_value()
            else:
              constants[k] = v

        subcomponents = {}
        for k, v in self.subcomponents.iteritems():
          subparams = {}
          for param, value in v["parameters"].iteritems():
            try:
              value = repr(value)
            except AttributeError:
              pass
            subparams[param] = value
          subcomponents[k] = {"class": v["class"], "parameters": subparams, "constants": v["constants"]}

        constraints = []
        for x in self.constraints:
          expr = repr(x)
          constraints.append(expr)

        connections = []
        for from_interface, to_interface, kwargs  in self.connections:
          new_args = {}
          for param, value in kwargs.iteritems():
            try:
              value = repr(value)
            except AttributeError:
              pass
            newArgs[param] = value
          connections.append([from_interface, to_interface, new_args])

        definition = {
            "parameters" : parameters,
            "constants" : constants,
            "subcomponents" : subcomponents,
            "constraints" : constraints,
            "connections" : connections,
            "interfaces" : self.interfaces,
        }

        if filename is not None:
            with open(join(ROCO_DIR, filename), "w") as fd:
                yaml.safe_dump(definition, fd)
        else:
            return yaml.safe_dump(definition)


    def get_subcomponent(self, name):
        """ Returns specified subcomponent of the component

        Args:
            name (str): name of the subcomponent to return

        Returns:
            the subcomponent with name 'name'

        Raises:
            KeyError: the subcomponent given by 'name' does not exist

        """
        return self.subcomponents[name]["component"]

    def constrain_subcomponent_parameter(self, (subcomponent, parameter), value):
        """ Constrains a parameter of subcomponent to the specified value

        Args:
            (subcomponent, parameter) (tuple (str, str)): name of subcomponent, and name of parameter to constrain
            value: Value of the parameter

        """
        self.subcomponents[subcomponent]["parameters"][parameter] = value

    def get_subcomponent_interface(self, component, name):
        """ Returns a subcomponent interface

        Args:
            component (str): name of the subcomponent
            name (str): name of the interface in that subcomponent

        Returns:
            the interface belonging to 'component' with name 'name'
        """
        return self.get_subcomponent(component).get_interface(name)

    def get_interface(self, name):
        """ Returns a interface of this component

        Args:
            name (str): name of the interface to return

        Returns:
            the interface with name 'name'
        """
        return self.interfaces[name]

    def set_interface(self, name, value):
        """ Sets a interface as passed in

        Args:
            name (str): name of the interface to set
            value: the value to set the interface to
        """
        if name in self.interfaces:
            self.interfaces[name] = value
        else:
            raise KeyError("Interface %s not initialized" % n)
        return self

    def assemble(self):
        """ Assembles the component

        """
        pass
        
    def append(self, name, prefix):
        """ Appends composables on each of the subcomponents to composable on current component

        Args:
            name (str): name of subcomponent
            prefix (str):

        """
        component = self.get_subcomponent(name)

        all_ports = set()
        for key in component.interfaces:
          ports = component.get_interface(key).ports
          if isinstance(ports, Port):
              all_ports.add(ports)
              if name not in self._prefixed:
                  ports.prefix(prefix)
              ports.update()
          else:
              all_ports.update(ports)
              for port in ports:
                  if name not in self._prefixed:
                      port.prefix(prefix)
                  port.update()
        for (key, composable) in component.composables.iteritems():
            if name not in self._prefixed:
                composable.prefixed = False
            else:
                composable.prefixed = True
            self.composables[key].append(composable, prefix)
        self._prefixed[name] = component

    def attach(self, interface1, interface2, kwargs):
        """ Attaches the specified ports on the subcomponents

        Args:
            (from_name, from_port) (tuple(str, str)): a tuple containing the name of the subcomponent, and the interface
                on the component to attach from
            (to_name, to_port) (tuple(str, str)): a tuple containing the name of the subcomponent, and the interface
                on the component to attach to
        """
        # Interfaces can contain multiple ports, so try each pair of ports
        if not isinstance(interface1.ports, (list, tuple)):
          interface1 = [interface1.ports]
        if not isinstance(interface2.ports, (list, tuple)):
          interface2 = [interface2.ports]
        if len(interface1) != len(interface2):
          if len(interface1) == 1:
            interface1 = interface1 * len(interface2)
          elif len(interface2) == 1:
            interface2 = interface2 * len(interface1)
          else:
            raise AttributeError("Number of ports in each interface don't match")

        for (port1, port2) in zip(interface1, interface2):
          self.extend_constraints(port1.constrain(self, port2, **kwargs))
          for (key, composable) in self.composables.iteritems():
            try:
                composable.attach(port1, port2, **kwargs)
            except:
                print "Error in attach:"
                print (from_name, from_port),
                print self.get_subcomponent_interface(from_name, from_port).name
                print (to_name, to_port),
                print self.get_subcomponent_interface(to_name, to_port).name
                raise

    def resolve_subcomponent(self, name):
        """ Creates subcomponent object and adds it to the current component

        Args:
            name: name of subcomponent to be created

        """
        sc = self.subcomponents[name]
        try:
          if sc["component"]:
            return
        except KeyError:
          pass

        c = sc["class"]
        try:
          kwargs = sc["constants"]
        except KeyError:
          kwargs = {}
        obj = get_subcomponent_object(c, name = prefix_string(self.get_name(), name), **kwargs)
        self.subcomponents[name]["component"] = obj
        self.inherit_parameters(obj, name)
        self.inherit_constraints(obj)


    def resolve_subcomponents(self):
        """Calls resolve_subcomponent on all subcomponents

        Args:
            None

        """
        for name in self.subcomponents:
            self.resolve_subcomponent(name)

    def inherit_constraints(self, subcomponent):
        """Inherits the constraints from a subcomponent

        Args:
            subcomponent (str): name of subcomponent to inherit from

        """
        self.extend_constraints(subcomponent.get_constraints())

    def eval_constraints(self):
        """Evaluates all the constraints imposed on subcomponents

        Args:
            None

        """
        for subcomponent in self.subcomponents.iterkeys():
            for (parameter_name, value) in self.subcomponents[subcomponent]["parameters"].iteritems():
                  self.set_parameter(prefix_string(subcomponent, parameter_name), value)
        
    def eval_subcomponents(self):
        """ Creates composables in current component based on composables in each of the subcomponents, then
            appends composables in subcomponents to corresponding composable in component

        """
        for (name, sc) in self.subcomponents.iteritems():
            obj = sc["component"]
            classname = sc["class"]
            try:
                #obj.make()
                for (key, composable) in obj.composables.iteritems():
                    if key not in self.composables:
                        self.composables[key] = composable.new()
                self.append(name, name)
            except:
                print "Error in subclass %s, instance %s" % (classname, name)
                raise
        # Let composables know what components exist
        # TODO remove this when we have a better way of letting composables
        # know about components that have no ports (ex Bluetooth module driver)
        for (key, composable) in self.composables.iteritems():
          for (name, sc) in self.subcomponents.iteritems():
            composable.add_component(sc["component"])

    def eval_interfaces(self):
        """ Adds interfaces to composables

        """
        for i in self.interfaces.iteritems():
            for (key, composable) in self.composables.iteritems():
                composable.add_interface(i)

    def eval_connections(self):
        """ Attaches each of the ports between which a connection was made

        """
        for (from_interface, to_interface, kwargs) in self.connections.itervalues():
            self.attach(from_interface,
                        to_interface,
                        kwargs)

    def make(self):
        """ Evaluates subcomponents, connections, and constraints, then assembles the component

        """
        self.reset()
        self.resolve_subcomponents()
        self.eval_constraints()

        self.eval_subcomponents()    # Merge composables from all subcomponents and tell them my components exist
        self.eval_interfaces()    # Tell composables that my interfaces exist
        self.eval_connections()   # Tell composables which interfaces are connected
        self.assemble()
        self.solve()
        self.check_constraints()

    def reset(self):
        """Resets component to a state before make is called.

        """
        pass

    def make_component_hierarchy(self):
        """Creates and returns a hierarchical representation of the component.

        """
        self.resolve_subcomponents()
        hierarchy = {}
        for n, sc in self.subcomponents.iteritems():
            hierarchy[n] = {"class":sc["class"], "subtree":sub.make_component_hierarchy()}
        return hierarchy

    def make_component_tree(self, file_name, tree_name="Root"):
        """Creates a image depicting the component tree

        Args:
            file_name (str): filename to write image to
            tree_name (str): name of the tree

        """
        import pydot
        graph = pydot.Dot(graph_type='graph')
        mynode = pydot.Node(root, label = root)
        self.recurse_component_tree(graph, mynode, root)
        graph.write_png(fn)

    def recurse_component_tree(self, graph, my_node, my_name):
        """Helper function to recurse down component tree to create it

        Args:
            graph (pydot.Dot): graph to add all the nodes to.
            my_node (pydot.Node): current node that is being added and will be recursed upon.
            my_name (str): name of the tree.

        """
        import pydot
        self.resolve_subcomponents()
        for n, sc in self.subcomponents.iteritems():
            fullstr = myname + "/" + n
            subnode = pydot.Node(fullstr, label = sc["class"] + r"\n" + n)
            graph.add_node(subnode)
            edge = pydot.Edge(mynode, subnode)
            graph.add_edge(edge)
            sub.recurse_component_tree(graph, subnode, fullstr)

    def make_output(self, file_dir=".", **kwargs):
        """Creates output based on the kwargs

        Args:
            file_dir (str): directory to store output
            kwargs (dict): arguments dictating which output to make

        """
        def kw(arg, default=False):
            if arg in kwargs:
                return kwargs[arg]
            return default

        print "Compiling robot designs..."
        sys.stdout.flush()
        if kw("remake", True):
            self.make()
        print "done."

        # XXX: Is this the right way to do it?
        import os
        try:
            os.makedirs(filedir)
        except:
            pass

        # Process composables in some ordering based on type
        ordered_types = ['electrical', 'ui', 'code'] # 'code' needs to know about pins chosen by 'electrical', and 'code' needs to know about IDs assigned by 'ui'
        # First call makeOutput on the ones of a type whose order is specified
        for composable_type in ordered_types:
            if composable_type in self.composables:
                self.composables[composable_type].make_output(filedir, **kwargs)
        # Now call makeOutput on the ones whose type did not care about order
        for (composable_type, composable) in self.composables.iteritems():
            if composable_type not in ordered_types:
                self.composables[composable_type].make_output(filedir, **kwargs)

        if kw("tree"):
            print "Generating hierarchy tree... ",
            sys.stdout.flush()
            self.make_component_tree(filedir + "/tree.png")
            print "done."
        print

        print "Happy roboting!"

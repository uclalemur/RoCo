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
from roco.api.utils.variable import Variable, eval_equation

from roco import ROCO_DIR
from roco.utils.utils import prefix as prefix_string
from roco.utils.utils import try_import, to_camel_case
from roco.utils.io import load_yaml
from sympy import Symbol, Eq, StrictGreaterThan, GreaterThan, StrictLessThan, LessThan
from roco.api.port import Port
from roco.api.interface import Interface
from roco.api.connection import Connection
from roco.api.parameterized import Parameterized
from ast import literal_eval as make_tuple

def get_subcomponent_object(component, name=None, **kwargs):
    """Function to generate an instantiated component from the class name.

    Args:
        component (str): The name of the component class to instantiate. Such as 'Rectangle'
        name (:obj:`str`, optional): The name to set for the component.
        **kwargs: Arbitrary keyword arguments to pass into the constructor.

    Returns:
        The instantiated component.

    """
    try:
        obj = try_import(component, to_camel_case(component))  ## Camelcase is to change 'hi_hello' into 'HiHello'.##
        c = obj(name=name, **kwargs)  ## can't find obj ##
        c.set_name(name)
        return c
    except AttributeError:
        obj = try_import(component, component.upper())
        c = obj(name=name, **kwargs)
        c.set_name(name)
        return c
    except ImportError:
        c = Component(component, **kwargs)
        c.set_name(name)
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

    def __init__(self, yaml_file=None, name=None, **kwargs):
        """Constructs a new Component object.

        Creates a Component that is either blank or loaded from a yaml file.

        Args:
            yaml_file (str): The optional yaml file to load the component information from.
            **kwargs: Arbitrary keyword arguments to control construction.

        """
        Parameterized.__init__(self, name=name)

        self.subcomponents = {}   ## Initially, there is no subcomponent. ##
        self.connections = {}
        self.tabs = []       ## tabs can add tab and slot to two faces to connect them. ##
        self.interfaces = {}
        self._prefixed = {}
        self.composables = OrderedDict() ## the OrderedDict can memberize the order that items are input.##
        self.attribute_params = {}
        self.hierarchical_constraints = {}

        if yaml_file:
            self._from_yaml(yaml_file)   ## '_from_yaml' can import yaml file from sources other than library. ##

        # Override to define actual component
        self.define(**kwargs)  ## doesn't any thing.##

        self.make()  ## don't know 'make()' ##


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
        try:
            if string.lower() == "false" or string.lower() == "true":
                return string.lower() == "true"
            expr = math.sympify(string)
            subs = []
            for a in expr.atoms(math.Symbol):
              subs.append((a, self.get_parameter(repr(a))))
            expr = expr.subs(subs)
            return expr
        except:
            return string

    def _from_yaml(self, file_name):
        """Loads in component information from a YAML file.

        Args:
            file_name (str): The name of the yaml file.

        """
        definition = load_yaml(file_name)

        try:
          for name, value in definition["subcomponents"].iteritems():
            try:
              # XXX Can these be sympy functions as well?
              kwargs = value["constants"]
            except AttributeError:
              kwargs = {}
            self.add_subcomponent(name, value["class"], **kwargs)
        except AttributeError: pass

        # keys are (parameters, constants, subcomponents, constraints, connections, interfaces)
        try:
          for name, default in definition["parameters"].iteritems():
              if not name in self.parameters:
                self.add_parameter(name, default)
        except AttributeError: pass

        try:
          for name, default in definition["constants"].iteritems():
            self.add_constant(name, default)
        except AttributeError: pass

        try:
          for name, value in definition["subcomponents"].iteritems():
              try:
                  for param, pvalue in value["parameters"].iteritems():
                      self.constrain_subcomponent_parameter((name, param), self._str_to_sympy(pvalue))
              except AttributeError:
                  pass
        except AttributeError: pass

        try:
          for value in definition["constraints"]:
            self.add_constraint(self._str_to_sympy(value))
        except (AttributeError, KeyError) : pass

        try:
          for value in definition["hierarchical_constraints"]:
              eqn =  self._str_to_sympy(value)
              self.hierarchical_constraints[eqn.lhs] = eqn.rhs
        except AttributeError: pass


        try:
            for from_port, to_port, kwargs in definition["connections"]:
                for param, pvalue in kwargs.iteritems():
                    try:
                        pvaluetup = make_tuple(pvalue)
                        if isinstance(pvaluetup, tuple):
                            kwargs[param] = tuple(self._str_to_sympy(x) for x in pvaluetup)
                        else:
                            kwargs[param] = self._str_to_sympy(pvalue)
                    except:
                        kwargs[param] = self._str_to_sympy(pvalue)
                self.add_connection(from_port, to_port, **kwargs)
        except AttributeError as e:
            pass

        try:
          for name, value in definition["interfaces"].iteritems():
            self.inherit_interface(name, value)
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
            object_type (str or type): code name of the subcomponent should 
            be python file/class or yaml name. 
            For example, you want to add a rectangle. You should call 
            instance.add_subcomponent('r1','Rectangle').

        """
        if name in self.subcomponents:
            raise ValueError("Subcomponent with name {} already exists".format(name))
        sc = {"class": object_type, "parameters": {}, "constants": kwargs, "component": None}
        self.subcomponents.setdefault(name, sc)
        self.resolve_subcomponent(name)
        if 'flip' in kwargs and kwargs['flip']:
            self.subcomponents[name]['component'].flip()

    def flip(self):
        if 'graph' in self.composables:
            self.composables['graph'].flip()

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
        if "graph" in self.composables.keys():
            del self.composables['graph']
        if name in self._prefixed:
            del self._prefixed[name]
        for sc in self.subcomponents:
            if 'graph' in self.subcomponents[sc]['component'].composables:
                self.subcomponents[sc]['component'].composables['graph'].placed = False

    def add_attribute_param(self, name, value, is_literal=False, desc="", **kwargs):
        """Adds an attribute parameter to the component. Attributes are special parameters
        which describe some inherent characteristic of the component, which may be often
        variable between different instances of the component, but can/should not be changed
        between makes of the same component instance. Thus, it is recommended these be set
        before calling make or adding connections to the component. Added Attributes will
        be returned by get_attribute_params, but they are merely a soft restriction for the user,
        and behave otherwise identically to parameters.

        Args:
            name (str): the parameter name
            value (int): an integer representing the default value for the
                parameter
            is_literal (bool): if True, the parameter's value will
                be stored as is. Else, it will be stored in a variable whose value
                can be changed.
            desc (str): a description of the attributes purpose
            **kwargs (dict): kwargs for the creation of the Dummy

        Returns:
            The newly added parameter

        Raises:
            KeyError: A parameter called name has already been created
            ValueError: Invalid characters in name
        """
        self.attribute_params[name] = desc
        return self.add_parameter(name, value, is_literal, **kwargs)

    def get_attribute_params(self):
        return self.attribute_params

    def add_hierarchical_constraint(self, (subcomponent, parameter), value):
        """Adds a hierarchical constraint to component

        Args:
            subcomponent (str): component name to constrain
            parameter (str): parameter of subcomponent to constrain
            value (Expression): expression to constrain to

        """
        self.hierarchical_constraints[self.get_parameter(prefix_string(subcomponent, parameter))] = value

    def get_hierarchical_constraints(self):
        """Returns a dictionary of hierarchical constraints
        """
        return self.hierarchical_constraints

    def extend_hierarchical_constraints(self, hier_constraints):
        """Extends the list of hierarchical constraints with the input list

            Args:
                constraints (dict): dictionary of new hierarchical constraints to add

        """

        for (var, val) in hier_constraints.iteritems():
            self.hierarchical_constraints[var] = val

    def inherit_parameters(self, other, prefix):
        """Adds parameters from another parameterized object to the current component.
        Overrides original fucntion in parameterized to account for attribute parameters

        Args:
            other (Parameterized): the parameterized object to inherit
                parameters from
            prefix (str): a prefix string to be added to the name of inherited
                parameters
        """
        attribute_params = {}
        try:
            attribute_params = other.get_attribute_params()
        except:
            pass

        for name, variable in other.all_parameters():
            if isinstance(variable, Variable):
                variable.set_name(prefix_string(prefix,variable.get_name()))
            if name in attribute_params.keys():
                self.add_attribute_param(prefix_string(prefix, name), variable, is_literal=True, desc=attribute_params[name])
            else:
                self.add_parameter(prefix_string(prefix, name), variable, is_literal=True)

    def del_parameter(self, name):
        """Removes the parameter with the given name

        Args:
            name (str): the parameter name

        Returns:
            The removed parameter with the given name

        Raises:
            KeyError: A parameter called name does not exist
        """
        try:
            self.attribute_params.pop(name)
        except:
            pass
        return Parameterized.del_parameter(self, name)


    def add_interface(self, name, interface, wrap_interface=True):
        """Adds an interface to this component.

        Args:
            name (str): unique identifier for interface that will be added to the component.
            ports (Port or list of Ports or Interface): the value that the new interface takes on.
            wrap_interface: If true, interface will be wrapped in an interface object
        """
        if name in self.interfaces:
            raise ValueError("Interface %s already exists" % name)
        if wrap_interface:
            new_interface = Interface(name, interface)
        else:
            new_interface = interface
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
        new_interface = Interface(name, self.get_subcomponent_interface(subcomponent,subname).get_ports(), (subcomponent, subname))
        self.interfaces.setdefault(name, new_interface)
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
        # self.connections[name] = [self.get_subcomponent_interface(from_interface[0], from_interface[1]),
        #                           self.get_subcomponent_interface(to_interface[0], to_interface[1]), kwargs]

        # print 'the value of connections is', self.connections[name]
        from_int = self.get_subcomponent_interface(from_interface[0], from_interface[1])
        to_int = self.get_subcomponent_interface(to_interface[0], to_interface[1])
        self.connections[name] = [Interface(from_int.get_name(), from_int.get_ports(), from_interface),
                                  Interface(to_int.get_name(), to_int.get_ports(), to_interface), kwargs]

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
                parameters[k] = repr(v.get_default_value())
            else:
                constants[k] = repr(v)

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
        for x in self.constraints.itervalues():
          expr = repr(x)
          constraints.append(expr)

        hierarchical_constraints = []
        for (var, val) in self.hierarchical_constraints.iteritems():
            hierarchical_constraints.append(repr(Eq(var, val)))

        connections = []
        for from_interface, to_interface, kwargs in self.connections.itervalues():
          new_args = {}
          for param, value in kwargs.iteritems():
            try:
              value = repr(value)
            except AttributeError:
              pass
            new_args[param] = value
          connections.append([from_interface.get_inheritance(), to_interface.get_inheritance(), new_args])

        definition = {
            "parameters" : parameters,
            "constants" : constants,
            "subcomponents" : subcomponents,
            "hierarchical_constraints" : hierarchical_constraints,
            "constraints" : constraints,
            "connections" : connections,
            "interfaces" : {name: interface.get_inheritance() for (name, interface) in self.interfaces.iteritems()},
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
        self.add_hierarchical_constraint((subcomponent, parameter), value)

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

    def set_interface(self, name, interface, wrap_interface=True):
        """ Sets a interface as passed in

        Args:
            name (str): name of the interface to set
            value: the value to set the interface to

        """
        if wrap_interface:
            new_interface = Interface(name, interface)
        else:
            new_interface = interface
        if name in self.interfaces:
            self.interfaces[name] = new_interface
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

    def attach(self, interface1, interface2, **kwargs):
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
        if len(interface1.ports) != len(interface2.ports):
            if len(interface1.ports) == 1:
                interface1 = interface1 * len(interface2.ports)
            elif len(interface2.ports) == 1:
                interface2 = interface2 * len(interface1.ports)
            else:
                raise AttributeError("Number of ports in each interface don't match")

        for (port1, port2) in zip(interface1.ports, interface2.ports):
            self.extend_constraints(port1.constrain(self, port2, **kwargs))
            for (key, composable) in self.composables.iteritems():
                try:
                    composable.attach(port1, port2, **kwargs)
                except:
                    print "Error in attach:"
                    print "interface 1: ", interface1.name
                    print "interface 2: ", interface2.name
                    raise

    def get_composable(self, name):
        """ Returns the composable referred to by 'name'

        Args:
            name (str): name of composable to return

        Returns:
            Composable object referred to by 'name'

        Raises:
            KeyError: Composable given by name does not exist

        """
        return self.composables[name]

    def resolve_subcomponent(self, name):
        """ Creates subcomponent object and adds it to the current component

        Args:
            name: name of subcomponent to be created

        """
        sc = self.subcomponents[name]
        try:
          if sc["component"]:   ## 'component' is none. why do we need to do it? ##
            return
        except KeyError:
          pass

        c = sc["class"]    ## sc['class'] is the object_type. ##
        try:
          kwargs = sc["constants"]  ## in case the 'constants' dose not exist. ##
        except KeyError:
          kwargs = {}
        obj = get_subcomponent_object(c, name = prefix_string(self.get_name(), name), **kwargs) ## Prefix_string = Prefix ##
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
        self.extend_hierarchical_constraints(subcomponent.get_hierarchical_constraints())
        self.extend_constraints(subcomponent.get_constraints().itervalues())

    def eval_hierarchical_constraints(self):
        """Evaluates all the constraints imposed on subcomponents

        Args:
            None

        """
        for (var, val) in self.hierarchical_constraints.iteritems():
            var.set_solved(eval_equation(val))

    def eval_subcomponents(self):
        """ Creates composables in current component based on composables in each of the subcomponents, then
            appends composables in subcomponents to corresponding composable in component

        """
        for (name, sc) in self.subcomponents.iteritems():
            obj = sc["component"]
            classname = sc["class"]
            try:
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
                        **kwargs)

    def make(self):
        """ Evaluates subcomponents, connections, and constraints, then assembles the component

        """
        ## Can't understand why we need make(). ##
        self.reset()     ## pass? why? ##
        self.resolve_subcomponents()
        self.eval_hierarchical_constraints()
        self.eval_subcomponents()    # Merge composables from all subcomponents and tell them my components exist
        self.eval_interfaces()    # Tell composables that my interfaces exist
        self.eval_connections()   # Tell composables which interfaces are connected
        self.assemble()      ## do nothing? ##
        self.solve()        ## ? ##
        self.check_constraints()   ## do nothing again? ##

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
            fullstr = my_name + "/" + n
            subnode = pydot.Node(fullstr, label = sc["class"] + r"\n" + n)
            graph.add_node(subnode)
            edge = pydot.Edge(my_node, subnode)
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
        sys.stdout.flush()  ## flush the buffering, thus we can see the output in real time without buffering. ##
        if kw("remake", True):  ## do self.make() if 'remake' in kwargs or 'True' ?##
            self.make()
        print "done."

        # XXX: Is this the right way to do it?
        import os
        try:
            os.makedirs(file_dir)   ## Almost the same as mkdir except this func can create the whole path. ##
        except:
            pass

        # Process composables in some ordering based on type
        ## the graph is not among them. ##
        ordered_types = ['electrical', 'ui', 'code'] # 'code' needs to know about pins chosen by 'electrical', and 'code' needs to know about IDs assigned by 'ui'
        # First call makeOutput on the ones of a type whose order is specified
        for composable_type in ordered_types:
            if composable_type in self.composables:
                self.composables[composable_type].make_output(file_dir, **kwargs)
        # Now call makeOutput on the ones whose type did not care about order
        for (composable_type, composable) in self.composables.iteritems():  ## focus on the format of composable. ##
            if composable_type not in ordered_types:
                self.composables[composable_type].make_output(file_dir, **kwargs)

        if kw("tree"):
            print "Generating hierarchy tree... ",
            sys.stdout.flush()
            self.make_component_tree(file_dir + "/tree.png")
            print "done."
        print

        print "Happy roboting!"

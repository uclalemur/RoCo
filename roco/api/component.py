"""Component class and helper function.

This module contains the Component class, as well as a helper function to load
components.

"""

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

    def _make_test(self, protobuf=False, display=True):
        """Constructs a test version of the Component.

        Sets test parameters as defined by the Component and creates output.

        Args:
            protobuf (Boolean): Whether to construct a protobuf or not.
            display (Boolean): Whether to display the output or not.

        """

    def _str_to_sympy(self, string):
        """Converts string to sympy expression

        Uses this Component's parameters to convert a string to a sympy expression.

        Args:
            string (str): The string to convert

        Returns:
            The sympy expression.

        """

    def _from_yaml(self, file_name):
        """Loads in component information from a YAML file.

        Args:
            file_name (str): The name of the yaml file.

        """

    def define(self, **kwargs):
        """Function for overriding interfaces.

        Args:
            **kwargs: Arbitrary keyword arguments

        """

    def add_subcomponent(self, name, object_type, **kwargs):
        """Adds a subcomponent to this Component.

        Args:
            name (str): unique identifier to refer to this subcomponent by
            object_type (str or type): code name of the subcomponent should be python file/class or yaml name

        """

    def del_subcomponent(self, name):
        """Deletes a subcomponent to this Component and performs any cleanup necessary

        Args:
            name (str): unique identifier of subcomponent to delete

        """

    def add_parameter_constraint(self, (subcomponent, parameter_name), constraint):
        """Constraints subcomponent parameter.

        Args:
            (subcomponent, parameter_name) (tuple(str,str)): a tuple representing a subcomponent a related parameter
                to constrain.
            constraint (Number or sympy expression): the constraint to impose on the subcomponent parameter.

        """


    def add_connection(self, (from_name, from_interface), (to_name, to_interface), **kwargs):
        """ Specifies interfaces on subcomponents to be connected

        Args:
            (from_name, from_interface) (tuple(str, str)): a tuple containing the name of the subcomponent, and the
                name of the interface the connection comes from
            (to_name, to_interface) (tuple(str, str)): a tuple containing the name of the subcomponent, and the
                name of the interface the connection goes to

        """

    def to_yaml(self, filename):
        """ Generates YAML file containing component information

        Args:
            filename (str): name of the yaml file to be generated
        """

    def assemble(self):
        """ Assembles the component

        """

    def append(self, name, prefix):
        """ Appends composables on each of the subcomponents to composable on current component

        Args:
            name (str): name of subcomponent
            prefix (str):


        """

    def attach(self, (from_name, from_port), (to_name, to_port), kwargs):
        """ Attaches the specified ports on the subcoponents

        Args:
            (from_name, from_port) (tuple(str, str)): a tuple containing the name of the subcomponent, and the interface
                on the component to attach from
            (to_name, to_port) (tuple(str, str)): a tuple containing the name of the subcomponent, and the interface
                on the component to attach to
        """

    def resolveSubcomponent(self, name):
        """ Creates subcomponent object and adds it to the current component

        Args:
            name: name of subcomponent to be created

        """

    def evalComponents(self):
        """ Creates composables in current component based on composables in each of the subcomponents, then
            appends composables in subcomponents to corresponding composable in component

        """

    def evalInterfaces(self):
        """ Adds interfaces to composables

        """


    def evalConnections(self):
        """ Attaches each of the ports between which a connection was made

        """

    def make(self):
        """ Evaluates subcomponents, connections, and constraints, then assembles the component

        """





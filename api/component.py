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

    def _str_to_sympy(self, s):
        """Converts string to sympy expression

        Uses this Component's parameters to convert a string to a sympy expression.

        Args:
            s (str): The string to convert

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
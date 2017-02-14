"""Composable class

This module contains the Composable class, meant to be derived by any classes
meant to be used to produce output
"""
class Composable():
    """Composable is an interface for objects which produce outputs

    Any class meant to produce output usable for the final robot designs should
    derive from this class. In any derived class, all member functions may be
    redefined.
    """

    def new(self):
        """Returns a new instance of a Composable.

        Args:
            None

        Returns:
            Composable object.

        """
        return self.__class__()

    def append(self, new_composable, new_prefix):
        """Combines two composables with the new one being prefixed.

        Args:
            new_composable (Composable): the composable that is being appended to this one.
            new_prefix (str): the prefix of all the names for the composable being appended.

        """
        raise NotImplementedError

    def add_component(self, component_obj):
        """Tells composable about what component it belongs to.

        Args:
            component_obj (Component): the component to tie this composable to.

        """
        pass

    def add_interface(self, new_interface):
        """Tells composable about an interface

        Args:
            new_interface: interface to add to composable.

        """
        pass

    def attach(self, from_port, to_port, **kwargs):
        """Attaches two ports inside the composable together

        Args:
            from_port (Port):
            to_port(Port):
            kwargs (dict): args relating to the connection between the ports.
        :return:
        """
        raise NotImplementedError

    def make_output(self, file_dir, **kwargs):
        """Creates output for the composable.

        Args:
            file_dir (str): the directory to place to output
            kwargs (dict): arguments for the output generation

        """
        raise NotImplementedError

"""Code Composable class

This module contains the Code Composable class, which is derived from the Virtual
Composable class. It is meant to be derived by any classes that produce code of
any language.
"""
class CodeComposable(VirtualComposable):
    """Virtual Composable is an interface for objects which produce code.

    Any class meant to produce code usable for the final robot designs should
    derive from this class. In any derived class, all member functions may be
    redefined."""

    def new(self):
        """Returns a new instance of a CodeComposable, identical to this one.

        Args:
            None

        Returns:
            Code Composable object.

        """
        pass

    def __init__(self, meta):
        """Initializes a Code Composable.

        Args:
            meta (dict): A Dictionary containing information about the code pertaining
            to this composable. meta Dictionary contains a list of all the targets supported
            and all the code for each target.

        """
        pass

    def addComponent(self, componentObj):
        """Tells composable about what component it belongs to.

        Args:
            component_obj (Component): the component to tie this composable to.

        """
        pass

    def removeTarget(self, target):
        """Removes a target from the list of supported targets.

        Args:
            target (Composable): The target to be removed from the meta.

        """
        pass

    def append(self, newComposable, newPrefix):
        """Combines two composables with the new one being prefixed.

        Args:
            new_composable (Composable): the composable that is being appended to this one.
            new_prefix (str): the prefix of all the names for the composable being appended.

        """
        raise NotImplementedError

    def subParameter(self, token, value):
        """Sets the subParameter for each target supported by the composable

        Args:
            token (any): key of the subParameter
            value (any): value of the subParameter

        """
        pass
        
    def attach(self, fromPort, toPort, kwargs):
        """Attaches two ports inside the composable together

        Args:
            from_port (Port):
            to_port(Port):
            kwargs (dict): args relating to the connection between the ports.
        :return:
        """
        raise NotImplementedError

    def makeOutput(self, filedir, **kwargs):
        """Creates output for the composable.

        Args:
            file_dir (str): the directory to place to output
            kwargs (dict): arguments for the output generation

        """
        raise NotImplementedError

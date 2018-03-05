"""Target class and helper functions.

This module contains the Target class as well as functions that convert the data
within the Code Composable into specific languages that the targets will output.
This class does nothing by itself. It needs to be extended to add any and all
functionality.

"""

class Target(object):

    def __init__(self, composable, meta, name=""):
        """Constructs a new Target Component.

        Args:
            composable (Composable): The Composable object that should be turned into code.
            meta (:obj:`str`, optional): A dictionary containing the different parts of the code.
            name (str): Name of the component.

        Returns:
            The instantiated component.

        """
        self.composable = composable
        self.meta = meta
        self.name = name


    def __str__(self):
        """Returns the string representation of the object.

        Args:
            None.

        Returns:
            The string representation of the object.

        """
        return "Target"

    def mangle(self, name):
        """Unmangles all the variable names in the Code Composable so that they can
        be reused for other components.

        Args:
            name (str): The name of the component.

        Returns:
            None.

        Raises:
            NotImplementedError

        """
        raise NotImplementedError

    def append(self, new_meta):
        """Appends the code of a different composable to this target.

        Args:
            new_meta (:obj:`str`, optional): A dictionary containing the different parts of the code.

        Returns:
            None.

        Raises:
            NotImplementedError

        """
        raise NotImplementedError

    def attach(self, from_port, to_port, **kwargs):
        """Attaches two ports in the component and replaces their symbolic
        representation in the target with real code.

        Args:
            from_port (OutPort): An output port that outputs into the parent component.
            to_port (InPort): An input port that takes the from_port as an input in the parent component.
            **kwargs: Arbitrary keyword arguments to control construction.

        Returns:
            None.

        Raises:
            NotImplementedError

        """
        raise NotImplementedError

    def makeOutput(self, filedir, **kwargs):
        """Converts the Code Componsable into source code and writes it to a
        specified file.

        Args:
            filedir (str): Path for the output file.
            **kwargs: Arbitrary keyword arguments to control construction.

        Returns:
            None.

        Raises:
            NotImplementedError

        """
        raise NotImplementedError

if __name__ == "__main__":
    pass
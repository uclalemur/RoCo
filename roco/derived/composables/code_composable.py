from roco.api.composable import Composable
from roco.derived.composables.virtual_composable import VirtualComposable
from roco.derived.ports.code_port import CodePort

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
        new_meta = {}
        for (target, meta) in self.meta.iteritems():
            new_meta[target] = target(self, meta).new()
        return self.__class__(new_meta)

    def __init__(self, meta):
        """Initializes a Code Composable.

        Args:
            meta (dict): A Dictionary containing information about the code pertaining
            to this composable. meta Dictionary contains a list of all the targets supported
            and all the code for each target.

        """
        VirtualComposable.__init__(self)
        self.meta = meta
        self.components = set()

    def add_component(self, component_obj):
        """Tells composable about what component it belongs to.

        Args:
            component_obj (Component): the component to tie this composable to.

        """
        self.components.add(component_obj)

    def remove_target(self, target):
        """Removes a target from the list of supported targets.

        Args:
            target (Composable): The target to be removed from the meta.

        """
        self.meta.pop(target)

    def append(self, new_composable, new_prefix):
        """Combines two composables with the new one being prefixed.

        Args:
            new_composable (Composable): the composable that is being appended to this one.
            new_prefix (str): the prefix of all the names for the composable being appended.

        """
        to_remove = []
        for (target, meta) in self.meta.iteritems():
            try:
                self.meta[target] = target(self, meta).append(new_composable.meta[target])
            except KeyError:
                print("Target: %s not supported!" % str(target(self, meta)))
                to_remove.append(target)

        self.components = self.components.union(new_composable.components)

    def sub_parameter(self, token, value):
        """Sets the subParameter for each target supported by the composable

        Args:
            token (any): key of the subParameter
            value (any): value of the subParameter

        """
        for (target, meta) in self.meta.iteritems():
            if meta is None:
                continue
            self.meta[target] = target(self, meta).sub_parameter(token, value)

    def attach(self, from_port, to_port, **kwargs):
        """Attaches two ports inside the composable together

        Args:
            from_port (Port):
            to_port(Port):
            kwargs (dict): args relating to the connection between the ports.

        """
        if not isinstance(from_port, CodePort) or not isinstance(to_port, CodePort):
            return

        if not from_port.can_mate(to_port) or not to_port.can_mate(from_port):
            raise Exception("%s cannot mate with %s!" % (from_port.__class__, to_port.__class__))

        for (target, meta) in self.meta.iteritems():
            self.meta[target] = target(self, meta).attach(from_port, to_port, **kwargs)

    def make_output(self, file_dir, **kwargs):
        from roco.derived.components.code_component import CodeComponent
        """Creates output for the composable.

        Args:
            file_dir (str): the directory to place to output
            kwargs (dict): arguments for the output generation

        """
        subs = {}
        for component in self.components:
            if isinstance(component, CodeComponent):
                subs.update(component.get_token_subs())


        for (target, meta) in self.meta.iteritems():
            self.meta[target] = target(self,meta).sub_parameters(subs)

        for (target, meta) in self.meta.iteritems():
            target(self, meta).make_output(file_dir, **kwargs)

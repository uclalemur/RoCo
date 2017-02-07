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
        return self.__class__()

    def append(self, new_composable, new_prefix):
        raise NotImplementedError

    def add_component(self, component_obj):
        pass

    def add_interface(self, new_interface):
        pass

    def attach(self, from_port, to_port, kwargs):
        raise NotImplementedError

    def make_output(self, file_dir, **kwargs):
        raise NotImplementedError

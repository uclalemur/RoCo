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

    def append(self, newComposable, newPrefix):
        raise NotImplementedError

    def addComponent(self, componentObj):
        pass

    def addInterface(self, newInterface):
        pass

    def attach(self, fromPort, toPort, kwargs):
        raise NotImplementedError

    def makeOutput(self, filedir, **kwargs):
        raise NotImplementedError

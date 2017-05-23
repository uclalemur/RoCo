from roco.api.component import Component
from roco.derived.composables.code_composable import CodeComposable
from roco.derived.ports.code_port import CodePort

class CodeComponent(Component):

    def __init__(self, yaml_file=None, name = None, **kwargs):
        """Initializes an empty Code Component if yaml_file is None, or a
        composite code component if yaml_file is a valid Composite Component File.

        Args:
            yaml_file (string): Path to a YAML file that contains the structure
                                for a composite component.
            **kwargs: Arbitrary keyword arguments to control construction.


        """
        self.meta = dict()
        Component.__init__(self, yaml_file, name, **kwargs)

    def define(self, **kwargs):
        """Function for overriding interfaces.

        Args:
            **kwargs: Arbitrary keyword arguments

        """
        self.add_parameter("target", "", is_symbol=False)

    def get_modified_name(self):
        """Function that returns modified name without any '.'

        Args:
            None

        """
        name = self.get_name() + str(id(self))
        return name.replace(".", "_")

    def mangle_names(self):
        """Mangle all global variable and parameter names in the code to a component
        specific string so that no variable names collide.

        Args:
            None

        """
        new_meta = {}
        name = self.get_modified_name()

        for (target, meta) in self.meta.iteritems():
            new_meta[target] = target(None, meta).mangle(name)

        for (iname, interface) in self.interfaces.iteritems():
            if isinstance(interface.ports[0], CodePort):
                interface.ports[0].mangle(name)

        return new_meta

    def get_token_subs(self):
        """Returns a dictionary containing all key value pairs for parameters.

        Returns:
            Dictionary of all parameters and their values

        """
        subs = dict()
        for (param, val) in self.parameters.iteritems():
            subs[param + "_" + self.get_modified_name()] = str(val)
        return subs

    def assemble(self):
        """Assemble the component by merging the code of all subcomponents together
            into one CodeComposable

        """
        self.composables['code'] = CodeComposable(self.mangle_names())

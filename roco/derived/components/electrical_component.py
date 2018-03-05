from roco.api.component import Component
from roco.derived.composables.electrical_composable import ElectricalComposable


class ElectricalComponent(Component):

    def __init__(self, yaml_file=None, name=None, **kwargs):
        """Initializes an empty Code Component if yaml_file is None, or a
        composite code component if yaml_file is a valid Composite Component File.

        Args:
            yaml_file (string): Path to a YAML file that contains the structure
                                for a composite component.
            **kwargs: Arbitrary keyword arguments to control construction.


        """
        Component.__init__(self, yaml_file=None, name=name, **kwargs)
        # self.physical = dict()
        # self.pin_indices = dict()


    def pin_indices(self, pins):
        """Returns an array containing 0's of length "pins"

        Args:
            pin (integer): Number of pins on ElectricalComponent

        """
        return [0 for i in pins]

    def assemble(self):
        """Assemble the component by merging the code of all subcomponents together
            into one ElectricalComposable

        """
        self.composables['electrical'] = ElectricalComposable(self.get_name(), self.physical)

if __name__ == "__main__":
    pass
    
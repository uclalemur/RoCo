from roco.derived.composables.container_composable import ContainerComposable

class ElectricalContainer(ContainerComposable):

    def new(self):
        new_container = ElectricalContainer()
        new_container.virtuals = self.virtuals
        return new_container

    def __init__(self, name, num_pins=0):
        ContainerComposable.__init__(self)
        self.physical = {
            name: {
                "connections": [None] * num_pins,
                "power": {
                    "Vin": [],
                    "Ground": [],
                    "pullDown": False,
                    "pullUp": False
            },
                "virtual": False
            }
        }

    def addVirtual(self, virtual_name, container_name, virtual, connections):
        virtual_name = self.remove_prefix(virtual_name)
        container_name = self.remove_prefix(container_name)
        for connect in connections:
            self.physical[container_name]["connections"][connect[0]] = [connect[1][0], connect[1][1], False]
        self.virtuals[virtual_name] = virtual

    def attach(self, from_port, to_port, **kwargs):
        pass

    def append(self, new_composable, new_prefix):
        ContainerComposable.append(self, new_composable, new_prefix)

    def make_output(self, file_dir, **kwargs):
        pass

if __name__ == "__main__":
    pass
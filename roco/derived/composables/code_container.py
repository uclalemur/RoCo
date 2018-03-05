from roco.derived.composables.container_composable import ContainerComposable

class CodeContainer(ContainerComposable):

    def new(self):
        new_container = CodeContainer()
        new_container.virtuals = self.virtuals
        return new_container

    def add_virtual(self, name, virtual, pin):
        self.virtuals[name] = pin
        virtual.set_container(self)

    def attach(self, from_port, to_port, **kwargs):
        pass

    def append(self, new_composable, new_prefix):
        ContainerComposable.append(self, new_composable, new_prefix)

    def make_output(self, file_dir, **kwargs):
        pass

if __name__ == "__main__":
    pass
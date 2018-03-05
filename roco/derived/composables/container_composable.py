from roco.api.composable import Composable

class ContainerComposable(Composable):

    def new(self):
        new_container = ContainerComposable()
        new_container.virtuals = self.virtuals
        # for (virtual, pin) in self.virtuals.iteritems():
        #     virtual.setContainer(newContainer)
        return new_container

    def __init__(self, meta=None):
        self.virtuals = dict()

    def attach(self, from_port, to_port, **kwargs):
        pass

    def append(self, new_composable, new_prefix):
        self.virtuals.update(new_composable.virtuals)

    def add_virtual(self, name, virtual, pin):
        self.virtuals[name] = pin
        virtual.set_container(self)

    def get_pin(self, name):
        return self.virtuals[name]

    def make_output(self, file_dir, **kwargs):
        return

if __name__ == "__main__":
    pass
"""Cpp Target class and helper functions.

This module contains the CppTarget class as well as functions that help convert
the data within the Code Composable into C++.

"""

from roco.api.target import Target
from re import findall

class Cpp(Target):

    @staticmethod
    def tokenize(label):
        """Marks the input label for mangling.

        Args:
            label (str): String to be mangled.

        Returns:
            The mangled string.

        """
        return "<<" + label + ">>"

    @staticmethod
    def detokenize(token):
        """Unmangles the given token.

        Args:
            token (str): String to be unmangled.

        Returns:
            The original unmangled string.

        """
        return token[2:-2]

    @staticmethod
    def new():
        """Returns a new empty meta dictionary.

        Args:
            None.

        Returns:
            A new empty meta dictionary.

        """
        return {"code": "", "declarations": "", "inputs": {}, "outputs": {}, "needs": set()}

    def __str__(self):
        """Returns the string representation of the target.

        Args:
            None.

        Returns:
            The string representation of the target.

        """
        return "Cpp"

    def getParamsFrom(self, where):
        """Returns an array containing the unmangled versions of all the mangled
        parameter tokens in a given string.

        Args:
            where (str): A string containing mangled tokens.

        Returns:
            An array containing the unmangled parameters in a given string.

        """
        return [self.detokenize(s) for s in findall("<<[0-9a-zA-Z]+?>>", where)]

    def mangle(self, name):
        """Unmangles all the variable names in the Code Composable so that they can
        be reused for other components.

        Args:
            name (str): The name of the component.

        Returns:
            None.
        """
        self.meta["code"] = self.meta["code"].replace("@@name@@", name)
        self.meta["declarations"] = self.meta["declarations"].replace("@@name@@", name)

        for (key, val) in self.meta["inputs"].iteritems():
            if val is not None:
                n_val = self.meta["inputs"].pop(key).replace("@@name@@", name)
                self.meta["inputs"][key.replace("@@name@@", name)] = n_val
            else:
                self.meta["inputs"][key.replace("@@name@@", name)] = self.meta["inputs"].pop(key)

        for (key, val) in self.meta["outputs"].iteritems():
            if val is not None:
                n_val = self.meta["outputs"].pop(key).replace("@@name@@", name)
                self.meta["outputs"][key.replace("@@name@@", name)] = n_val
            else:
                self.meta["outputs"][key.replace("@@name@@", name)] = self.meta["outputs"].pop(key)

        return self.meta

    def get_parameters(self):
        """Returns an array of all the parameters used in the code

        Args:
            None.

        Returns:
            A string array of all the parameters in the code.

        """
        output_parameters = []
        input_parameters = []
        code_parameters = self.getParamsFrom(self.meta["code"])

        for (key, val) in self.meta["inputs"].iteritems():
            input_parameters += self.getParamsFrom(val)

        for (key, val) in self.meta["outputs"].iteritems():
            output_parameters += self.getParamsFrom(val)

        return list(set(output_parameters) | set(input_parameters) | set(code_parameters))

    def append(self, new_meta):
        """Appends the code of a different composable to this target.

        Args:
            new_meta (:obj:`str`, optional): A dictionary containing the different parts of the code.

        Returns:
            None.

        """
        p_new_line = "" if not self.meta["code"] else "\n"

        if new_meta["code"]:
            self.meta["code"] += p_new_line + new_meta["code"]

        self.meta["inputs"].update(new_meta["inputs"])
        self.meta["outputs"].update(new_meta["outputs"])
        self.meta["needs"].update(new_meta["needs"])
        self.meta["declarations"] += new_meta["declarations"]
        return self.meta

    def get_inputs(self, output_label):
        """Returns an array containing all the inputs used for a given output.

        Args:
            output_label (str): The output for which inputs are returned.

        Returns:
            An array of strings containing the inputs used for the output named output_label.

        """
        return [self.detokenize(s) for s in findall("<<[0-9a-zA-Z_]+?>>", self.meta["outputs"][output_label])]

    def replace_input(self, output_label):
        inputs = self.get_inputs(output_label)
        for input in inputs:
            if input in self.meta["inputs"] and self.meta["inputs"][input] is not None:
                token = self.tokenize(input)
                sub = self.meta["inputs"][input]
                self.meta["outputs"][output_label] = self.meta["outputs"][output_label].replace(token, sub)
                self.meta["code"] = self.meta["code"].replace(token, sub)

    def replace_all_inputs(self):
        for output_label, output_expr in self.meta["outputs"].iteritems():
            self.replace_input(output_label)
        for input_token, input_sub in self.meta["inputs"].iteritems():
            if input_sub is not None:
                token = self.tokenize(input_token)
                self.meta["code"] = self.meta["code"].replace(token, input_sub)

    def sub_parameters(self, subs):
        for (token, sub) in subs.iteritems():
            for output_token, output_expr in self.meta["outputs"].iteritems():
                self.meta["outputs"][output_token] = output_expr.replace(self.tokenize(token), sub)
            self.meta["code"] = self.meta["code"].replace(self.tokenize(token), sub)
        return self.meta

    def attach(self, from_port, to_port, kwargs):
        """Attaches two ports in the component and replaces their symbolic
        representation in the target with real code.

        Args:
            from_port (OutPort): An output port that outputs into the parent component.
            to_port (InPort): An input port that takes the from_port as an input in the parent component.
            **kwargs: Arbitrary keyword arguments to control construction.

        Returns:
            None.
        """
        input_label = to_port.get_label()
        output_label = from_port.get_label()

        try:
            # Substitute all in the necessary inputs into the output specified by output_label
            self.replace_input(output_label)

            # Substitute output specified by output_label into the input specified by input_label
            if self.meta["inputs"][input_label] is None:
                self.meta["inputs"][input_label] = self.meta["outputs"][output_label]

            # Substitute all inputs into the appropriate outputs
            self.replace_all_inputs()

            self.meta["inputs"].pop(input_label)
            self.meta["outputs"].pop(output_label)
        except KeyError:
            pass

        return self.meta

    def make_output(self, filedir, **kwargs):
        """Converts the Code Componsable into source code and writes it to a
        specified file.

        Args:
            filedir (str): Path for the output file.
            **kwargs: Arbitrary keyword arguments to control construction.

        Returns:
            None.
        """
        self.replace_all_inputs()

        filename = "%s/main.cpp" % filedir
        f = open(filename, "w")

        for include in self.meta["needs"]:
            f.write("#include <" + include + ">\n")

        f.write("\n\n")
        f.write(self.meta["declarations"])
        f.write("\n\n")
        f.write(self.meta["code"])

        main = "\nint main()\n" + \
                "{\n" + \
                "   %s\n" % "".join([s + ";\n" for (k,s) in self.meta["outputs"].iteritems() if s]) + \
                "   return 0;\n" + \
                "}\n\n"

        f.write(main)
        f.close()

from roco.derived.composables.target.target import Target
import os
from re import findall, compile
import errno

class Web(Target):
    @staticmethod
    def new():
        """Returns a new empty meta dictionary.

        Args:
            None.

        Returns:
            A new empty meta dictionary.

        """
        return {
            "script": "",
            "declarations": "",
            "functions: "
            "inputs": {},
            "outputs": {},
            "needs": set(),
        }

    def __init__(self, composable, meta, name="", params={}):
        Target.__init__(self, composable, meta, name, params)
        self.parameters = params
        if "script" not in self.meta.keys():
            self.meta["script"] = ""
        if "declarations" not in self.meta.keys():
            self.meta["declarations"] = ""
        if "functions" not in self.meta.keys():
            self.meta["functions"] = ""
        if "inputs" not in self.meta.keys():
            self.meta["inputs"] = {}


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

    def eval_output(self, parameters):
        self.replace_all_params(parameters)

    def restore_params(self, str, parameters):
        p = compile("@@param@@(.*?)@@")
        matches = p.findall(str)
        for i in matches:
            str = str.replace("@@param@@{}@@".format(i), parameters[i].get_value())
        return str

    def __str__(self):
        """Returns the string representation of the target.

        Args:
            None.

        Returns:
            The string representation of the target.

        """
        return "Web"


    def sub_parameters(self, subs):
        # for input_token, inputSub in self.meta["inputs"].iteritems():
        #    if token == input_token:
        #        self.meta["inputs"][token] = pSub
        for (token, sub) in subs.iteritems():
            for output_token, output_expr in self.meta["outputs"].iteritems():
                tok = self.tokenize(token)
                if tok in output_expr:
                    self.meta["outputs"][output_token] = output_expr.replace(tok, sub)

            self.meta["script"] = self.meta["script"].replace(self.tokenize(token), sub)
            self.meta["declarations"] = self.meta["declarations"].replace(self.tokenize(token), sub)
            self.meta["functions"] = self.meta["functions"].replace(self.tokenize(token), sub)
        return self.meta

    def get_params_from(self, where):
        """Returns an array containing the unmangled versions of all the mangled
        parameter tokens in a given string.

        Args:
            where (str): A string containing mangled tokens.

        Returns:
            An array containing the unmangled parameters in a given string.

        """
        return [self.detokenize(s) for s in findall("<<[0-9a-zA-Z]+?>>", where)]

    def mangle(self, name):
        """Unmangles all the variable names in the script Composable so that they can
        be reused for other components.

        Args:
            name (str): The name of the component.

        Returns:
            None.
        """
        dec = []
        self.meta["declarations"] = self.meta["declarations"].replace("@@name@@", name)
        self.meta["script"] = self.meta["script"].replace("@@name@@", name)
        self.meta["functions"] = self.meta["functions"].replace("@@name@@", name)

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
        """Returns an array of all the parameters used in the script

        Args:
            None.

        Returns:
            A string array of all the parameters in the script.

        """
        output_parameters = []
        input_parameters = []
        script_parameters = self.get_params_from(self.meta["script"])

        for (key, val) in self.meta["inputs"].iteritems():
            input_parameters += self.get_params_from(val)

        for (key, val) in self.meta["outputs"].iteritems():
            output_parameters += self.get_params_from(val)

        return list(set(output_parameters) | set(input_parameters) | set(script_parameters) | set(
            self.get_params_from(self.meta["declarations"])) | set(self.get_params_from(self.meta["functions"])))

    def append(self, new_meta):
        """Appends the script of a different composable to this target.

        Args:
            new_meta (:obj:`str`, optional): A dictionary containing the different parts of the script.

        Returns:
            None.

        """
        p_new_line = "" if not self.meta["script"] else "\n"

        if new_meta["script"]:
            self.meta["script"] += p_new_line + new_meta["script"]

        self.meta["inputs"].update(new_meta["inputs"])
        self.meta["outputs"].update(new_meta["outputs"])
        self.meta["needs"].update(new_meta["needs"])
        self.meta["declarations"] += (new_meta["declarations"] + "\n")
        self.meta["functions"] += (new_meta["functions"] + "\n")
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
                self.meta["script"] = self.meta["script"].replace(token, sub)
                self.meta["declarations"] = self.meta["declarations"].replace(token, sub)
                self.meta["functions"] = self.meta["functions"].replace(token, sub)

    def replace_all_inputs(self):
        for output_label, output_expr in self.meta["outputs"].iteritems():
            self.replace_input(output_label)
        for input_token, input_sub in self.meta["inputs"].iteritems():
            if input_sub is not None:
                token = self.tokenize(input_token)
                self.meta["script"] = self.meta["script"].replace(token, input_sub)
                self.meta["declarations"] = self.meta["declarations"].replace(token, sub)
                self.meta["functions"] = self.meta["functions"].replace(token, sub)

    def replace_all_params(self, parameters):
        self.meta["script"] = self.restore_params(self.meta["script"], parameters)
        self.meta["declarations"] = self.restore_params(self.meta["declarations"], parameters)
        self.meta["functions"] = self.restore_params(self.meta["functions"], parameters)
        for k, v in self.meta["outputs"].iteritems():
            self.meta["outputs"][k] = self.restore_params(v, parameters)

    def sub_parameters(self, subs):
        for (token, sub) in subs.iteritems():
            for output_token, output_expr in self.meta["outputs"].iteritems():
                self.meta["outputs"][output_token] = output_expr.replace(self.tokenize(token), sub)

            self.meta["declarations"] = self.meta["declarations"].replace(self.tokenize(token), sub)
            self.meta["script"] = self.meta["script"].replace(self.tokenize(token), sub)
        return self.meta

    def attach(self, from_port, to_port, **kwargs):
        """Attaches two ports in the component and replaces their symbolic
        representation in the target with real script.

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
        """Converts the script Composable into source script and writes it to a
        specified file.

        Args:
            filedir (str): Path for the output file.
            **kwargs: Arbitrary keyword arguments to control construction.

        Returns:
            None.
        """
        self.replace_all_inputs()

        if filedir[-1] == "/":
            filedir += "main"
        else:
            filedir += "/main"

        filename = "%s/main.html" % filedir

        if not os.path.exists(filename):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        f = open(filename, "w")

        head = ("<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                "\t<meta charset=utf-8 />\n"
                "\t<title>whooo control robots</title>\n"
                "\n"
                "\t<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">\n"
                "\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">\n"
                "</head>\n"
                "\n")
        f.write(head)
        body = ("<body>\n"
                "\t<h1>Yay Robots!</h1>\n"
                "\n")
        declarations = self.meta["declarations"].replace("\n", "\n\t")
        body = body + declarations + "\n\n"
        logDeclaration =   ("\t<table class=wslog> <tr>\n"
                            "\t\t\t<td width=\"50%\" valign=\"top\">\n"
                            "\t\t\t\t<div id=\"wsRx\" class=\"log\"></div>\n"
                            "\t\t\t</td>\n"
                            "\t\t\t<td width=\"50%\" valign=\"top\">\n"
                            "\t\t\t\t<div id=\"wsTx\" class=\"log\"></div>\n"
                            "\t\t\t</td>\n"
                            "\t</tr></table>\n")
        body = body + logDeclaration

        f.write(body)

        functions =   ("\t<script>\n\n"
                    "\t\twindow.onload = function () {\n")
        functions = functions + "\t\t\t" + self.meta["functions"].replace("\n", "\n\t\t\t") + "\n\t\t}\n"

        f.write(functions)

        
        script = ("\t\tvar wsRx = document.getElementById(\"wsRx\");\n"
                           "\t\tvar wsTx = document.getElementById(\"wsTx\");\n"
                           "\t\tfunction rxLog(text) {\n"
                           "\t\t\twsRx.innerHTML = text + wsRx.innerHTML.split(\"<br>\").slice(0, 4).join(\"<br>\") ;\n"
                           "\t\t}\n"
                           "\t\tfunction txLog(text) {\n"
                           "\t\t\twsTx.innerHTML = text + wsTx.innerHTML.split(\"<br>\").slice(0, 4).join(\"<br>\") ;\n"
                           "\t\t}\n"
                           "\n"
                           "\t\t/* WebSocket utilities */\n"
                           "\t\tvar connection = new WebSocket('ws://'+location.hostname+':81/', ['arduino']);\n"
                           "\t\tconnection.onopen = function(){\n"
                           "\t\t\tvar timeStr = new Date().toLocaleTimeString();\n"
                           "\t\t\tvar text = \"(\" + timeStr + \") : CONNECTED <br>\";\n"
                           "\t\t\tconnection.send('Connect ' + new Date()); \n"
                           "\t\t\ttxLog(text);\n"
                           "\t\t};\n"
                           "\t\tconnection.onerror = function(error){\n"
                           "\t\t\tvar timeStr = new Date().toLocaleTimeString();\n"
                           "\t\t\tvar text = \"(\" + timeStr + \") : EE = \" + error + \"<br>\";\n"
                           "\t\t\tconsole.log('WebSocket Error ', error);\n"
                           "\t\t\ttxLog(text);\n"
                           "\t\t};\n"
                           "\t\tconnection.onmessage = function(e){\n"
                           "\t\t\tvar timeStr = new Date().toLocaleTimeString();\n"
                           "\t\t\tvar text = \"(\" + timeStr + \") : RX = \" + e.data + \"<br>\";\n"
                           "\t\t\tconsole.log('Server: ', e.data);\n"
                           "\t\t\trxLog(text);\n"
                           "\t\t};\n"
                           "\n")
        script = script + "\t\t" + self.meta["script"].replace("\n", "\n\t\t") + "\n\n"

        script = script + "\n" + "\t</script>\n\n\t</body>\n</html>"
        f.write(script)
        f.close()

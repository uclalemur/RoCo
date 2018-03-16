from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.web_target import Web


class WebButton(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.add_parameter("buttonValue", "UP")
        self.meta = {
            Web: {
                "script":  ("function @@name@@Send(val) {\n"
                            "\tvar timeStr = new Date().toLocaleTimeString();\n"
                            "\tvar text = \"(\" + timeStr + \") : TX = #\" + val + \"<br>\";\n"
                            "\ttxLog(text);\n"
                            "\n"
                            "\tconsole.log('Button pressed, sending #'+val); \n"
                            "\tconnection.send('#'+val);\n"
                            "}\n"
                            "\n"
                            "function @@name@@Release() {\n"
                            "\tvar timeStr = new Date().toLocaleTimeString();\n"
                            "\tvar text = \"(\" + timeStr + \") : TX = #0<br>\";\n"
                            "\ttxLog(text);\n"
                            "\tconsole.log('Button released'); \n"
                            "\tconnection.send('#0');\n"
                            "}\n"
                            "\n"),
                "declarations": "\t<td><button id=\"@@name@@\"    name=\"@@name@@\" value=\"@@param@@buttonValue@@\" class=\"smbutton\">@@param@@buttonValue@@</button></td>\n",
                "functions": ("var btns = document.getElementsByName(\"@@name@@\");\n"
                            "for (var i = 0; i < btns.length; i++) {\n"
                            "\t\tbtns[i].ontouchstart = function(e) {@@name@@Send(this.value); e.stopPropagation(); e.preventDefault();};\n"
                            "\t\tbtns[i].onmousedown = function(e) {@@name@@Send(this.value); e.stopPropagation(); e.preventDefault();};\n"
                            "\t\tbtns[i].ontouchend = function() {@@name@@Release(); e.stopPropagation(); e.preventDefault();}\n"
                            "\t\tbtns[i].onmouseup = function() {@@name@@Release(); e.stopPropagation(); e.preventDefault();}\n"
                            "}\n"),
                "inputs": {},
                "outputs": {"sentValue_@@name@@": "@@name@@_receivedString",
                },
                "needs": set(),
            }
        }
        CodeComponent.define(self, **kwargs)

    def assemble(self):
        # print self.get_parameter("variable_name").get_value()
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = WebButton(name = "but")
    ss.make_output()

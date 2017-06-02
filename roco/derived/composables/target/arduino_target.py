from roco.derived.composables.target.cpp_target import Cpp
import os
import errno


class Arduino(Cpp):
    @staticmethod
    def new():
        return {
            "code": "",
            "declarations": "",
            "setup": "",
            "loop": "",
            "inputs": {},
            "outputs": {},
            "needs": set(),
            "interface": {
                "html": "",
                "style": "",
                "js": "",
                "event": "",
            }
        }

    def __init__(self, composable, meta, name=""):
        Cpp.__init__(self, composable, meta, name)
        if "interface" not in self.meta.keys():
            self.meta["interface"] = {
                "html": "",
                "style": "",
                "js": "",
                "event": ""
            }

        if "loop" not in self.meta.keys():
            self.meta["loop"] = ""

        if self.meta["interface"]["html"] or self.meta["interface"]["style"] or \
                self.meta["interface"]["js"] or self.meta["interface"]["event"]:
            self.interface = True
        else:
            self.interface = False

    def __str__(self):
        return "Arduino"

    def mangle(self, name):
        self.meta["setup"] = self.meta["setup"].replace("@@name@@", name)
        self.meta["loop"] = self.meta["loop"].replace("@@name@@", name)
        self.meta["interface"]["html"] = self.meta["interface"]["html"].replace("@@name@@", name)
        self.meta["interface"]["style"] = self.meta["interface"]["style"].replace("@@name@@", name)
        self.meta["interface"]["js"] = self.meta["interface"]["js"].replace("@@name@@", name)
        self.meta["interface"]["event"] = self.meta["interface"]["event"].replace("@@name@@", name)
        return Cpp.mangle(self, name)

    def append(self, new_meta):
        p_new_line = "" if not self.meta["setup"] else "\n"
        l_new_line = "" if not self.meta["loop"] else "\n"

        if new_meta["setup"]:
            if "Serial.begin" in new_meta["setup"] and "Serial.begin" in self.meta["setup"]:
                new_meta["setup"] = new_meta["setup"].replace("Serial.begin(115200)", "")
            self.meta["setup"] += p_new_line + new_meta["setup"]

        if new_meta["loop"]:
            self.meta["loop"] += l_new_line + new_meta["loop"]

        if new_meta["interface"]:
            h_new_line = "" if not self.meta["interface"]["html"] else "\n"
            s_new_line = "" if not self.meta["interface"]["style"] else "\n"
            j_new_line = "" if not self.meta["interface"]["js"] else "\n"
            e_new_line = "" if not self.meta["interface"]["event"] else "\n"

            self.meta["interface"]["html"] += h_new_line + new_meta["interface"]["html"]
            self.meta["interface"]["style"] += s_new_line + new_meta["interface"]["style"]
            self.meta["interface"]["js"] += j_new_line + new_meta["interface"]["js"]
            self.meta["interface"]["event"] += e_new_line + new_meta["interface"]["event"]

        return Cpp.append(self, new_meta)

    def get_parameters(self):
        return list(set(self.get_params_from(self.meta["interface"]["html"])) |
                    set(self.get_params_from(self.meta["interface"]["style"])) |
                    set(self.get_params_from(self.meta["interface"]["js"])) |
                    set(self.get_params_from(self.meta["interface"]["event"])) |
                    set(self.get_params_from(self.meta["setup"])) | set(self.get_params_from(self.meta["loop"])) |
                    Cpp.get_parameters(self))

    def sub_parameters(self, subs):
        # for input_token, inputSub in self.meta["inputs"].iteritems():
        #    if token == input_token:
        #        self.meta["inputs"][token] = pSub
        for (token, sub) in subs.iteritems():
            for output_token, output_expr in self.meta["outputs"].iteritems():
                tok = self.tokenize(token)
                if tok in output_expr:
                    self.meta["outputs"][output_token] = output_expr.replace(tok, sub)
            self.meta["code"] = self.meta["code"].replace(self.tokenize(token), sub)
            self.meta["setup"] = self.meta["setup"].replace(self.tokenize(token), sub)
            self.meta["loop"] = self.meta["loop"].replace(self.tokenize(token), sub)

            self.meta["interface"]["html"] = self.meta["interface"]["html"].replace(self.tokenize(token), sub)
            self.meta["interface"]["style"] = self.meta["interface"]["style"].replace(self.tokenize(token), sub)
            self.meta["interface"]["js"] = self.meta["interface"]["js"].replace(self.tokenize(token), sub)
            self.meta["interface"]["event"] = self.meta["interface"]["event"].replace(self.tokenize(token), sub)
        return self.meta

    def update_interface(self):
        self.meta["declarations"] = "const char *ssid = \"NodeMCU\";\n" + \
                                    "const char *password = \"password\";\n" + \
                                    "ESP8266WebServer server(80);\n" + \
                                    "WebSocketsServer wsServer = WebSocketsServer(81);\n" + \
                                    "\n" + \
                                    "const char *html = \"<!DOCTYPE html>\"\n" + \
                                    "\"<html>\"\n" + \
                                    "\"<head>\"\n" + \
                                    "\"<meta charset=utf-8 />\"\n" + \
                                    "\"<meta name = \\\"viewport\\\" content = \\\"width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;\\\">\"\n" + \
                                    "\"<style>\"\n" + \
                                    "\"%s\"" % (self.meta["interface"]["style"].replace("\n", "\"\n\"    ").rstrip()) + \
                                    "\n" + \
                                    "\"</style>\"\n" + \
                                    "\"</head>\"\n" + \
                                    "\"<body>\"\n" + \
                                    "\"%s\"\n" % (self.meta["interface"]["html"].replace("\n", "\"\n\"").rstrip()) + \
                                    "\"<script>\"\n" + \
                                    "\"%s\"\n" % (
                                        "    %s" % (
                                            self.meta["interface"]["js"].replace("\n", "\"\n\"    ").rstrip())) + \
                                    "\"    var connection = new WebSocket(\\\"ws://\\\"+location.hostname+\\\":81/\\\", [\\\"arduino\\\"]);\"\n" + \
                                    "\"\"\n" + \
                                    "\"    connection.onopen = function(){\"\n" + \
                                    "\"      console.log(\\\"Opened\\\");\"\n" + \
                                    "\"    };\"\n" + \
                                    "\"\"\n" + \
                                    "\"    connection.onerror = function(error){\"\n" + \
                                    "\"      console.log(error);\"\n" + \
                                    "\"    };\"\n" + \
                                    "\"\"\n" + \
                                    "\"    connection.onmessage = function(e){\"\n" + \
                                    "\"      console.log(e.data);\"\n" + \
                                    "\"    };\"\n" + \
                                    "\"\"\n" + \
                                    "\"    connection.onclose = function(e){\"\n" + \
                                    "\"      console.log(\\\"Closed\\\");\"\n" + \
                                    "\"    };\"\n" + \
                                    "\"</script>\"\n" + \
                                    "\"</body>\"\n" + \
                                    "\"</html>\";\n\n" + self.meta["declarations"]

        self.meta["code"] = "\nvoid handleRoot() {\n" + \
                            "    server.send(200, \"text/html\", html);" + \
                            "}\n" + \
                            "\n" + \
                            "void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t lenght) {\n" + \
                            "    switch(type){\n" + \
                            "        case WStype_DISCONNECTED:\n" + \
                            "            Serial.println(\"Disconnected!\");\n" + \
                            "            break;\n" + \
                            "        case WStype_CONNECTED:\n" + \
                            "        {\n" + \
                            "            IPAddress\n" + \
                            "            ip = wsServer.remoteIP(num);\n" + \
                            "            Serial.printf(\"[%u] Connected to %d.%d.%d.%d\", num, ip[0], ip[1], ip[2], ip[3], payload);\n" + \
                            "        }\n" + \
                            "            wsServer.sendTXT(num, \"Connected\");\n" + \
                            "            break;\n" + \
                            "        case WStype_TEXT:\n" + \
                            "            %s" % (
                                self.meta["interface"]["event"].replace("\n", "\n            ")).rstrip() + \
                            "\n            break;\n" + \
                            "    }\n" + \
                            "}\n" + self.meta["code"]

        self.meta["setup"] = self.meta["setup"].replace("Serial.begin(115200)", "")
        self.meta["setup"] = "\n" + \
                             "    Serial.begin(115200);\n" + \
                             "    WiFi.softAP(ssid, password);\n" + \
                             "    IPAddress myIP = WiFi.softAPIP();\n" + \
                             "    Serial.println(myIP);\n" + \
                             "\n" + \
                             "    wsServer.begin();\n" + \
                             "    wsServer.onEvent(webSocketEvent);\n" + \
                             "    server.on(\"/\", handleRoot);\n" + \
                             "    server.begin();\n" + \
                             "    if(MDNS.begin(\"arduino\")){\n" + \
                             "       Serial.println(\"MDNS Responder Started\");\n" + \
                             "    }\n" + \
                             "\n" + \
                             "    MDNS.addService(\"http\", \"tcp\", 80);\n" + \
                             "    MDNS.addService(\"ws\", \"tcp\", 81);\n" + \
                             "\n" + self.meta["setup"]

        self.meta["outputs"]["server"] = "server.handleClient()"
        self.meta["outputs"]["wsServer"] = "wsServer.loop()"

    def write_HTML(self):
        pass

    def make_output(self, filedir, **kwargs):
        self.replace_all_inputs()
        if self.interface:
            self.update_interface()


        if filedir[-1] == "/":
            filedir += "main"
        else:
            filedir += "/main"

        filename = "%s/main.ino" % filedir

        if not os.path.exists(filename):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        f = open(filename, "w")

        for include in self.meta["needs"]:
            f.write("#include <" + include + ">\n")

        f.write("\n\n")
        f.write(self.meta["declarations"])
        f.write("\n\n")
        f.write(self.meta["code"])

        setup = "\nvoid setup()\n" + \
                "{\n" + \
                "    %s\n" % self.meta["setup"] + \
                "}\n"

        loop = "\nvoid loop()\n" + \
               "{\n" + \
               "    %s\n" % self.meta["loop"] + \
               "    %s\n" % "".join([s + ";\n" for (k, s) in self.meta["outputs"].iteritems() if s]) + \
               "}\n"

        f.write(setup)
        f.write(loop)
        f.close()


from roco.derived.components.code_component import CodeComponent
from roco.derived.ports.string_port import OutStringPort
from roco.derived.ports.bool_port import OutBoolPort
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class WebSocket(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            Arduino: {
                "code":    ("void webSocketEvent(uint8_t id, WStype_t type, uint8_t * payload, size_t length) {\n"
                            "\n"
                            "\t\tswitch(type) {\n"
                            "\t\t\t\tcase WStype_DISCONNECTED:\n"
                            "\t\t\t\t\t\tDEBUG(\"Web socket disconnected, id = \", id);\n"
                            "\t\t\t\t\t\tbreak;\n"
                            "\t\t\t\tcase WStype_CONNECTED: \n"
                            "\t\t\t\t{\n"
                            "\t\t\t\t\t\t// IPAddress ip = webSocket.remoteIP(id);\n"
                            "\t\t\t\t\t\t// Serial.printf(\"[%u] Connected from %d.%d.%d.%d url: %s\\n\", id, ip[0], ip[1], ip[2], ip[3], payload);\n"
                            "\t\t\t\t\t\tDEBUG(\"Web socket connected, id = \", id);\n"
                            "\n"
                            "\t\t\t\t\t\t// send message to client\n"
                            "\t\t\t\t\t\twsSend(id, \"Connected to \");\n"
                            "\t\t\t\t\t\twsSend(id, ap_ssid);\n"
                            "\t\t\t\t\t\tbreak;\n"
                            "\t\t\t\t}\n"
                            "\t\t\t\tcase WStype_BIN:\n"
                            "\t\t\t\t\t\tDEBUG(\"On connection #\", id)\n"
                            "\t\t\t\t\t\tDEBUG(\"  got binary of length \", length);\n"
                            "\t\t\t\t\t\tfor (int i = 0; i < length; i++)\n"
                            "\t\t\t\t\t\t\tDEBUG(\"    char : \", payload[i]);\n"
                            "\n"
                            "\t\t\t\tcase WStype_TEXT:\n"
                            "\t\t\t\t\t\tDEBUG(\"On connection #\", id)\n"
                            "\t\t\t\t\t\tDEBUG(\"  got text: \", (char *)payload);\n"
                            "\n"
                            "\t\t\t\t\t\t@@name@@_payload = (char*) &payload;\n"
                            "\t\t\t\t\t\t@@name@@_isReceived = true;"
                            "\t\t\t\t\t\tbreak;\n"
                            "\t\t}\n"
                            "}\n"),
                "declarations":    ("#include <Hash.h>\n"
                                    "#include <FS.h>\n"
                                    "#include <ESP8266WiFi.h>\n"
                                    "#include <WiFiClient.h>\n"
                                    "#include <ESP8266WebServer.h>\n"
                                    "#include <WebSocketsServer.h>\n"
                                    "#include <ESP8266mDNS.h>\n"
                                    "#include \"debug.h\"\n"
                                    "#include \"file.h\"\n"
                                    "#include \"server.h\"\n"
                                    "// WiFi AP parameters\n"
                                    "char ap_ssid[13];\n"
                                    "char* ap_password = \"\";\n"
                                    "\n"
                                    "// WiFi STA parameters\n"
                                    "char* sta_ssid = \n"
                                    "\t\"...\";\n"
                                    "char* sta_password = \n"
                                    "\t\"...\";\n"
                                    "\n"
                                    "char* mDNS_name = \"paperbot\";\n"
                                    "\n"
                                    "String html;\n"
                                    "String css;\n"
                                    "char* @@name@@_payload;\n"
                                    "bool @@name@@_isReceived = false;\n"
                                    "void webSocketEvent(uint8_t id, WStype_t type, uint8_t * payload, size_t length);\n"),
                "setup":   ("\n"
                            "\t\tsprintf(ap_ssid, \"ESP_%08X\", ESP.getChipId());\n"
                            "\n"
                            "\t\tfor(uint8_t t = 4; t > 0; t--) {\n"
                            "\t\t\t\tSerial.printf(\"[SETUP] BOOT WAIT %d...\\n\", t);\n"
                            "\t\t\t\tSerial.flush();\n"
                            "\t\t\t\tLED_ON;\n"
                            "\t\t\t\tdelay(500);\n"
                            "\t\t\t\tLED_OFF;\n"
                            "\t\t\t\tdelay(500);\n"
                            "\t\t}\n"
                            "\t\tLED_ON;\n"
                            "\t\t//setupSTA(sta_ssid, sta_password);\n"
                            "\t\tsetupAP(ap_ssid, ap_password);\n"
                            "\t\tLED_OFF;\n"
                            "\n"
                            "\t\tsetupFile();\n"
                            "\t\thtml = loadFile(\"/controls.html\");\n"
                            "\t\tcss = loadFile(\"/style.css\");\n"
                            "\t\tregisterPage(\"/\", \"text/html\", html);\n"
                            "\t\tregisterPage(\"/style.css\", \"text/css\", css);\n"
                            "\n"
                            "\t\tsetupHTTP();\n"
                            "\t\tsetupWS(webSocketEvent);\n"
                            "\t\t//setupMDNS(mDNS_name);\n"
                            "\n"),
                "loop":    ("\n"
                            "\t\twsLoop();\n"
                            "\t\thttpLoop();\n"),
                "inputs": {
                },
                "outputs": {
                    "output_@@name@@": "@@name@@_payload"
                },
                "needs": set(),
                "interface": {
                    "html": "",
                    "style": "",
                    "js": "",
                    "event": "",
                }
            }
        }

        self.add_interface("payload", OutStringPort(self, "payload", "payload_@@name@@"))
        self.add_interface("isReceived", OutBoolPort(self, "isReceived", "isReceived_@@name@@"))

        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = WebSocket()
    ss.make_output()

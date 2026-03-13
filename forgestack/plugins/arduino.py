from forgestack.core.plugin_api import Plugin


class ArduinoPlugin(Plugin):
    def __init__(self):
        super().__init__("arduino", requires=["python"])

    def plan(self, ctx):
        ctx.plan.create_file(
            "device/README.md",
            template="arduino/device_README.md",
        )
        ctx.plan.create_file(
            "device/arduino/README.md",
            template="arduino/device_arduino_README.md",
        )
        ctx.plan.create_file(
            "device/arduino/sketch.ino",
            template="arduino/sketch.ino",
        )
        ctx.plan.create_file(
            "device/protocol/README.md",
            template="arduino/device_protocol_README.md",
        )


plugin = ArduinoPlugin()
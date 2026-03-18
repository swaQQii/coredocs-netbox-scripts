from extras.scripts import Script, StringVar


class HelloScript(Script):
    class Meta:
        name = "Hello Script"
        description = "Demonstrates inputs, logging, and commit switch"

    greeting_name = StringVar(required=False, label="Name")

    def run(self, inputs, commit):
        name = (inputs.get("greeting_name") or "world").strip()
        self.log_info(f"Hello, {name}!")
        return f"Greeting sent (commit={commit})"

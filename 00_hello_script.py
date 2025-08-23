from extras.scripts import Script, StringVar

class Hello(Script):
    class Meta:
        name = "Hello"
        description = "Demonstrates inputs, logging, and commit switch"

    greeting_name = StringVar(required=False, label="Name")

    def run(self, data, commit):
        name = (data.get("greeting_name") or "world").strip()
        self.log_info(f"Hello, {name}!")
        return f"Greeting sent (commit={commit})"

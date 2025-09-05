import click
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings

COMMANDS = []

class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        for cmd in COMMANDS:
            if cmd.startswith(text):
                yield Completion(cmd, start_position=-len(text))

kb = KeyBindings()
@kb.add('tab')
def _(event):
    buffer = event.app.current_buffer
    if buffer.complete_state:
        buffer.complete_next()
    else:
        buffer.start_completion(select_first=True)

@click.command()
def cli():
    session = PromptSession(completer=CommandCompleter(), key_bindings=kb)
    while True:
        try:
            cmd = session.prompt("nexcli> ")
            if cmd.strip().lower() in ("exit", "quit"):
                click.secho("Goodbye 👋", fg='green')
                break
            result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
            click.secho(result.stdout, fg='white')
            if result.stderr:
                click.secho(result.stderr, fg='red')
        except KeyboardInterrupt:
            click.echo("\nExiting.")
            break

if __name__ == "__main__":
    cli()

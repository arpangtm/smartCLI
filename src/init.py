from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.key_binding import KeyBindings
from llm import autocomplete_suggestion
from llm.model import question_answer
import subprocess
import click
import pyfiglet
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from questionaire import questionaire

console = Console()

COMMANDS = ['ls', 'echo', 'pwd', 'cat', 'exit']

class InlineCommandSuggest(AutoSuggest):
    def get_suggestion(self, buffer, document):
        text = document.text
        for cmd in COMMANDS:
            if cmd.startswith(text) and cmd != text:
                return Suggestion(cmd[len(text):])
            # else:
                # auto_command = autocomplete_suggestion(text)
                # if auto_command:
                #     return Suggestion(auto_command[len(text):])

kb = KeyBindings()
@kb.add('tab')
def _(event):
    buffer = event.app.current_buffer
    suggestion = buffer.suggestion

    if suggestion:
        buffer.insert_text(suggestion.text)
        buffer.suggestion = None

session = PromptSession(auto_suggest=InlineCommandSuggest(), key_bindings=kb)

def main():
    # clear screen

    subprocess.run("clear", shell=True, check=True, text=True, capture_output=True)
    setup_success = questionaire()
    if not setup_success:
        return
    subprocess.run("clear", shell=True, check=True, text=True, capture_output=True)
    banner_text = pyfiglet.figlet_format("NEXCLI", font="slant")
    banner_text = Align.center(banner_text)
    panel = Panel(banner_text, title="🎉 Welcome 🎉", style="bold cyan")
    console.print(panel)
    while True:
        try:
            command = session.prompt(">> ")
            try:
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                click.secho(result.stdout, fg='white')
            except subprocess.CalledProcessError as e:      
                res = question_answer({"error": e.stderr, "command": command})
                if res["question_type"] == "general":
                    click.secho(res["answer"], fg='white')
                elif res["question_type"] == "command":
                    setCommand(res["answer"])
                    

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

def setCommand(command):
    click.secho("This command you are looking for is probably:")
    click.secho(command, fg='green')
    if click.confirm("Do you want to execute this command?"):
        click.secho("Executing: " + command, fg='green')
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            click.secho(result.stdout, fg='white')
        except subprocess.CalledProcessError as e:
            click.secho("Error: " + e.stderr, fg='red')
    return
if __name__ == "__main__":
    main()


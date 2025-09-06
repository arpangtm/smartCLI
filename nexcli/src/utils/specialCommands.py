import click
import os

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


from rich.prompt import Prompt

from rich.align import Align

from nexcli.src.llm.model import image_question


console = Console()



class ImageProcessor:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}
    
    def is_image(self, file_path):
        return Path(file_path).suffix.lower() in self.supported_formats
    


def show_drop_zone():
    drop_zone = Panel(
        Align.center(
            Text.assemble(
                ("📸 ", "bold yellow"),
                ("DRAG & DROP ZONE", "bold white"),
                (" 📸\n\n", "bold yellow"),
                ("Drop your images here or paste file paths\n", "dim white"),
                ("Supported formats: JPG, PNG, GIF, BMP, TIFF, WebP\n\n", "dim cyan"),
                ("Type 'exit' to quit • 'help' for commands", "dim")
            ),
            vertical="middle"
        ),
        title="🎨 Image Drop CLI",
        title_align="center",
        border_style="bright_cyan",
        padding=(2, 4),
        height=12
    )
    console.print(drop_zone)


@click.command()
def ImageProcessing():

    
    processor = ImageProcessor()
    
    console.clear()

    # Interactive mode
    show_drop_zone()
    
    while True:
        try:
            console.print()
            user_input = Prompt.ask("🎯 Drop image:", 
                                    default="", show_default=False).strip()
            
            if not user_input:
                return
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                console.print("Exiting Image Mode...", style="bold cyan")
                break
            
            file_path = user_input.strip('"\'')
            
            if not os.path.exists(file_path):
                console.print(f"❌ File not found: {file_path}", style="red")
                console.print("💡 Tip: Drag and drop the file or paste the full path", style="dim")
                continue
            
            if not processor.is_image(file_path):
                console.print(f"❌ Not a supported image format: {Path(file_path).suffix}", 
                            style="red")
                continue
            
            user_request = Prompt.ask(
                "What do you want to ask about the image?",
                default='new'
            )

            response = image_question(file_path, user_request)
            console.print(response)
        
            
        except KeyboardInterrupt:
            console.print("Exiting Image Mode...", style="bold cyan")
            return
        except Exception as e:
            console.print(f"❌ Error: {str(e)}", style="red")


def nexCommand(command):
    if command == "!image":
        ImageProcessing()


if __name__ == "__main__":
    ImageProcessing()

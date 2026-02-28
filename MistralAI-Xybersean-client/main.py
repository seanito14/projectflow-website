import re
import os
import sys
import argparse
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from client import MistralAIClient
from agent import AgenticLoop

console = Console()

def main():
    parser = argparse.ArgumentParser(description="MistralAI-Xybersean-client: Agentic App Builder CLI")
    parser.add_index = True # Placeholder for future indexing features
    
    console.print(Panel.fit(
        "[bold cyan]Mistral AI - Xybersean Client[/bold cyan]\n"
        "[dim]Agentic App Builder | Powered by Mistral Large 3[/dim]",
        border_style="bright_blue"
    ))

    try:
        client = MistralAIClient()
        agent = AgenticLoop(client)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        console.print("[yellow]Hint: Ensure MISTRAL_API_KEY is set in a .env file.[/yellow]")
        sys.exit(1)

    while True:
        try:
            user_input = console.input("\n[bold green]❯[/bold green] ")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[dim]Goodbye![/dim]")
                break
            
            if user_input.lower() == "clear":
                agent.clear_history()
                console.print("[dim]Conversation history cleared.[/dim]")
                continue

            with console.status("[bold blue]Thinking...[/bold blue]", spinner="dots"):
                response = agent.run(user_input)
            
            console.print(Markdown(response))

            # App Builder: Detect and offer to save files
            files_found = re.findall(r"```(?:\w+)?\s*\n#\s*filename:\s*(.+)\n([\s\S]+?)\n```", response)
            for filename, content in files_found:
                filename = filename.strip()
                if console.confirm(f"\n[bold cyan]App Builder:[/bold cyan] Save generated code to [bold underline]{filename}[/bold underline]?"):
                    try:
                        with open(filename, "w") as f:
                            f.write(content.strip())
                        console.print(f"[bold green]✓[/bold green] Saved {filename}")
                    except Exception as e:
                        console.print(f"[bold red]Error saving file:[/bold red] {e}")

        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted. Type 'exit' to quit.[/dim]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()

import re
import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from client import MistralAIClient
from agent import AgenticLoop

console = Console()

def main():
    parser = argparse.ArgumentParser(description="MistralAI-Xybersean-client: Agentic App Builder CLI")
    
    console.print(Panel.fit(
        "[bold cyan]Mistral AI - Xybersean Client[/bold cyan]\n"
        "[dim]Agentic App Builder | Powered by Mistral Large 3[/dim]",
        border_style="bright_blue"
    ))

    # Check for API Key and prompt if missing
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        console.print("\n[yellow]MISTRAL_API_KEY not found or unconfigured.[/yellow]")
        api_key = console.input("[bold cyan]Please paste your Mistral API Key:[/bold cyan] ").strip()
        if not api_key:
            console.print("[bold red]Error: API Key is required to proceed.[/bold red]")
            sys.exit(1)
        
        # Save to .env
        env_path = ".env"
        with open(env_path, "w") as f:
            f.write(f"MISTRAL_API_KEY={api_key}\n")
            f.write(f"MISTRAL_MODEL=mistral-large-latest\n")
        
        # Reload env
        os.environ["MISTRAL_API_KEY"] = api_key
        console.print("[bold green]✓[/bold green] API Key saved to .env and configured.")

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
            
            if not user_input.strip():
                continue

            # Command handling
            if user_input.startswith("/"):
                cmd = user_input.strip().lower()
                if cmd in ["/exit", "/quit"]:
                    console.print("[dim]Goodbye![/dim]")
                    break
                elif cmd == "/clear":
                    agent.clear_history()
                    console.print("[dim]Conversation history and session tokens cleared.[/dim]")
                    continue
                elif cmd == "/stats":
                    console.print(Panel(
                        f"**Model:** {agent.client.model}\n"
                        f"**Total Session Tokens:** {agent.total_prompt_tokens + agent.total_completion_tokens:,}\n"
                        f"*(Prompts: {agent.total_prompt_tokens:,} | Completions: {agent.total_completion_tokens:,})*",
                        title="[bold magenta]⚡ Current Session Stats[/bold magenta]", border_style="magenta"
                    ))
                    continue
                elif cmd == "/save_chat":
                    try:
                        import json
                        with open("chat_log.json", "w") as f:
                            json.dump(agent.history, f, indent=2)
                        console.print("[bold green]✓[/bold green] Full chat history saved to `chat_log.json`")
                    except Exception as e:
                        console.print(f"[bold red]Failed to save chat:[/bold red] {e}")
                    continue
                elif cmd == "/help":
                    help_text = (
                        "**Commands:**\n"
                        "- `/help`: Show this help message\n"
                        "- `/clear`: Clear conversation history and reset tokens\n"
                        "- `/stats`: Show current session API token usage\n"
                        "- `/save_chat`: Dump the entire conversation history to a JSON file\n"
                        "- `/exit` or `/quit`: Exit the application\n\n"
                        "**App Builder:**\n"
                        "If the AI generates a code block with `# filename: example.txt` on the first line, "
                        "the CLI will automatically prompt you to save it."
                    )
                    console.print(Panel(Markdown(help_text), title="[bold yellow]🛠️ Mistral CLI Help[/bold yellow]", border_style="yellow"))
                    continue
                else:
                    console.print(f"[yellow]Unknown command '{cmd}'. Type /help for a list of commands.[/yellow]")
                    continue

            with console.status("[bold blue]Thinking...[/bold blue]", spinner="dots"):
                response_content, usage = agent.run(user_input)
            
            console.print(Panel(
                Markdown(response_content),
                title="[bold cyan]🤖 Mistral Assistant[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            ))

            if usage:
                # Handle both object (from API) and dict (from fallback)
                p_tokens = usage.prompt_tokens if hasattr(usage, 'prompt_tokens') else usage.get("prompt_tokens", 0)
                c_tokens = usage.completion_tokens if hasattr(usage, 'completion_tokens') else usage.get("completion_tokens", 0)

                table = Table(box=box.MINIMAL_DOUBLE_HEAD, show_header=False, expand=False, style="dim")
                table.add_column("Stat", style="bold yellow")
                table.add_column("Value", style="green")
                table.add_row("Model", agent.client.model)
                table.add_row("Prompt Tokens", f"{p_tokens:,}")
                table.add_row("Completion Tokens", f"{c_tokens:,}")
                table.add_row("Total Session Tokens", f"{agent.total_prompt_tokens + agent.total_completion_tokens:,}")
                
                console.print(Panel(table, title="[bold magenta]⚡ API Usage Stats[/bold magenta]", border_style="magenta", expand=False))

            # App Builder: Detect and offer to save files
            files_found = re.findall(r"```(?:\w+)?\s*\n#\s*filename:\s*(.+)\n([\s\S]+?)\n```", response_content)
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

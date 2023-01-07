import nextcord
from nextcord.ext import commands
from rich import print

class DiscordBot(commands.Bot):
    """
    Pre-configured Discord bot
    """
    def __init__(self, guild_id, command_prefix="!"):
        super().__init__(command_prefix=command_prefix, intents = nextcord.Intents.all())
        self.guild_id = guild_id
        
    async def on_ready(self):
        # indicate bot has loaded.
        print(f'[bold purple]DISCORD BOT:[/] Is ready.')
        # display Bot Info
        print(f'[bold purple]DISCORD BOT:[/] Tag is [bold magenta]{self.user}[/].')
        print(f'[bold purple]DISCORD BOT:[/] User Id is [bold magenta]{self.user.id}[/].')
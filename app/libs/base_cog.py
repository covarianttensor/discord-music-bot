import nextcord
from nextcord.ext import commands
from rich import print
import traceback
import sys

class BaseCog(commands.Cog):
    """
    Base cog class for this Discord bot.
    """
    def __init__(self, bot):
        self.bot = bot

    #==========================================================
    #=====================Helper Methods=======================
    #==========================================================

    #==========================================================
    #=========================EVENTS===========================
    #==========================================================

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event Handler Description:
        Performs actions once the cog is loaded.
        """
        # Indicate COG has loaded.
        print(f'[bold #f703e8 on #e8f703]DISCORD COG:[/] [italic #add8e6]{type(self).__name__}[/]: Loaded.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except nextcord.HTTPException:
                pass

        elif isinstance(error, commands.MissingRequiredArgument):
            #await ctx.send(error)
            print(error)

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    #==========================================================
    #========================TASKS=============================
    #==========================================================
    
    
  
  
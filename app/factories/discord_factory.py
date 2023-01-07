from libs.discord_bot import DiscordBot
from cogs import music

def create_instance(main_guild_id, command_prefix):
    """
    Returns a configured instance of a Discord bot.
    """
    # create a bot instance
    bot = DiscordBot(main_guild_id, command_prefix=command_prefix)
    # load cogs into bot instance
    cogs_to_add_to_bot = [music]
    for i in range(len(cogs_to_add_to_bot)):
        cogs_to_add_to_bot[i].setup(bot)
    # return bot instance
    return bot
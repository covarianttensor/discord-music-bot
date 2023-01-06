import os
from pathlib import Path
import factories.discord_factory as discord_factory
from configs import constants
from db import sql, models

# Start bot if module is program entry point.
if __name__ == '__main__':
    """
    Get Discord token from environment variable.
    DO NOT HARD CODE TOKENS INTO SOURCE CODE!!!
    """

    # Create missing directories
    Path("./app/cookies").mkdir(parents=True, exist_ok=True)
    Path("./app/cache").mkdir(parents=True, exist_ok=True)

    # Create all database models
    models.Base.metadata.create_all(bind=sql.engine)

    # create a discord bot instance using factory function
    if "prod" == os.environ["RUN_MODE"]:
        print("Running in production mode...")
        discord_bot = discord_factory.create_instance(
            constants.GUILD_ID_PRODUCTION,command_prefix=constants.COMMAND_PREFIX)
        discord_bot.run(os.environ["DISCORD_TOKEN_PROD"])
    else:
        print("Running in development mode...")
        discord_bot = discord_factory.create_instance(
            constants.GUILD_ID_DEV,command_prefix=constants.COMMAND_PREFIX)
        discord_bot.run(os.environ["DISCORD_TOKEN_DEV"])
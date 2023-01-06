import asyncio
import requests
from rich import print
import nextcord
from nextcord.ext import commands, tasks
from helpers.youtube import get_audio_info, get_audio_search_results, get_query_type
from lib.base_cog import BaseCog
from lib.music_classes import MusicTrack
from typing import Union, Dict, List
from configs.constants import ADMIN_ROLE_NAME

class Roles(BaseCog):
    """
    This cog helps to give or remove roles to users.
    """
    def __init__(self, bot):
        super().__init__(bot)

    #==========================================================
    #=====================Helper Methods=======================
    #==========================================================

    #==========================================================
    #=========================EVENTS===========================
    #==========================================================

    #==========================================================
    #========================TASKS=============================
    #==========================================================

    #==========================================================
    #=======================COMMANDS===========================
    #==========================================================

# === Module Method(s) ===
def setup(bot):
    """
    A module method to add this module's cog to a discord bot.
    To be used by a factory module.
    """
    bot.add_cog(Roles(bot))
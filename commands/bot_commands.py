import discord
from discord import app_commands

from src.Bot import Bot
from src.ticker.ticker_workflow import ticker_workflow

from src.logger import notify_bot

def define_commands(tree, bot: Bot):
    @tree.command(
        name = "info",
        description=f"retrieves information for particular coin"
    )
    @app_commands.describe(ticker=f"ticker for the coin you want info on, up to 8 chars")
    async def slash(interaction: discord.Interaction, ticker: str):
        await interaction.response.defer(thinking=True)
        
        if interaction.user.bot: return
        
        notify_bot(interaction, "ticker commmand used")
        await ticker_workflow(interaction, bot, ticker)
        notify_bot(interaction, "ticker complete")
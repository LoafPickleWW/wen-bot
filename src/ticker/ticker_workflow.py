import discord

from src.Bot import Bot
from src.ticker.TokenInfo import TokenInfo
from src.ticker.graph import get_graph
from src.ticker.utils import (
    calculate_percentage_change, get_ticker_info, 
    get_ticker_candles, find_highest_and_lowest
)

from src.logger import notify_admin

async def ticker_workflow(interaction: discord.Interaction, bot: Bot, ticker: str):
    try:
        # Get ticker/token data
        token: TokenInfo = await get_ticker_info(interaction, bot, ticker.lower())
        if token == None:
            await interaction.edit_original_response(content="Ticker not found")
            return None

        # Get candles for 7 days
        candles = await get_ticker_candles(interaction, token, 7)

        # Get candles for 24 days, only for the high/low
        candles_24 = await get_ticker_candles(interaction, token, 1)

        img_file = None
        if candles:
            highest_7d, lowest_7d = find_highest_and_lowest(candles)
            highest_24h, lowest_24h = find_highest_and_lowest(candles_24)
            img_file = get_graph(candles)
            
        # Price calculations
        change_24_hrs, change_7_days = calculate_percentage_change(token.price, token.price1d, token.price7d)
        
        # Make it pretty
        embed =  discord.Embed(
            title=f"Buy more ${token.ticker.lstrip('$')}",
            colour = discord.Colour.green(),
            url= f"https://vestige.fi/swap?asset_in=0&asset_out={token.asset_id}"
        )
        embed.add_field(name="Name", value=token.asset_name, inline=True)
        embed.add_field(name="Ticker", value=token.ticker, inline=True)
        embed.add_field(name="Rank", value=token.rank, inline=True)
        embed.add_field(name="Price", value=f"{token.price:,.8f} A", inline=False)

        embed.add_field(name="24h High", value=f"{highest_24h:,.8f} A", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="7d High", value=f"{highest_7d:,.8f} A", inline=True)
        
        embed.add_field(name="24h Low", value=f"{lowest_24h:,.8f} A", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="7d Low", value=f"{lowest_7d:,.8f} A", inline=True)

        embed.add_field(name="24h Price Change", value=f"{change_24_hrs:,.2f}%", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="7d Price Change", value=f"{change_7_days:,.2f}%", inline=True)
        
        embed.add_field(name="24h Volume", value=f"{token.volume1d:,.3f} A", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Market Cap", value=f"{token.market_cap:,.3f} A", inline=True)

        attachments = []    
        if img_file:
            embed.set_image(
                url="attachment://graph.png"
            )
            attachments.append(discord.File(img_file, "graph.png"))
        if token.image:
            embed.set_thumbnail(
                url=token.image
            )

        embed.set_footer(
            icon_url="attachment://vestige.png",
            text="Powered by Vestige, Built by evilcorp.algo"
        )
        attachments.append(discord.File(fp="./images/logo.png", filename="vestige.png"))
        
        await interaction.edit_original_response(embed=embed, attachments=attachments)
    except Exception as e:
        await interaction.edit_original_response(content="Something bad happened, and I need an adult...")
        await notify_admin(interaction, bot, f"Ticker: {ticker} :: Reason: {e}")
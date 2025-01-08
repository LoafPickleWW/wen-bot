import discord, copy

from src.ticker.utils import conversion

class TickerView(discord.ui.View):
    def __init__(self, message, currencies, current, token, timeout):
        super().__init__(timeout=timeout)
        self.message = message

        for currency, _ in currencies.items():
            if currency != current:
                self.add_currency_button(currency, currencies, token)

    def add_currency_button(self, currency, currencies, token):
        button = discord.ui.Button(
            label=currency, 
            style=discord.ButtonStyle.primary,
            custom_id=f"currency_{currency}"
        )
        
        async def btn_callback(interaction):
            await interaction.response.defer()
            await ticker_ui(interaction, currencies, currency, token)
            
        button.callback = btn_callback
        self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.message.user.id

    async def on_timeout(self):
        await self.message.edit_original_response(view=None)

async def ticker_ui(interaction, currencies, currency, token):
        
        converted_token = conversion(currencies, currency, token)

        # Make it pretty
        embed =  discord.Embed(
            title=f"Buy more ${token.ticker.lstrip('$')}",
            colour = discord.Colour.green(),
            url= f"https://vestige.fi/swap?asset_in=0&asset_out={token.asset_id}"
        )
        embed.add_field(name="Name", value=token.asset_name, inline=True)
        embed.add_field(name="Ticker", value=token.ticker, inline=True)
        embed.add_field(name="Rank", value=token.rank, inline=True)
        embed.add_field(name="Price", value=converted_token.price, inline=False)

        embed.add_field(name="24h Price Change", value=converted_token.change_24_hrs, inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="7d Price Change", value=converted_token.change_7_days, inline=True)

        embed.add_field(name="24h High", value=converted_token.highest_24h, inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="7d High", value=converted_token.highest_7d, inline=True)
        
        embed.add_field(name="24h Low", value=converted_token.lowest_24h, inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="7d Low", value=converted_token.lowest_7d, inline=True)
        
        embed.add_field(name="24h Volume", value=converted_token.volume1d, inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Market Cap", value=converted_token.market_cap, inline=True)

        attachments = []    
        if token.graph:
            token.graph.seek(0)
            embed.set_image(
                url="attachment://graph.png"
            )
            attachments.append(discord.File(token.graph, "graph.png"))
        if token.image:
            embed.set_thumbnail(
                url=token.image
            )

        embed.set_footer(
            icon_url="attachment://vestige.png",
            text="Powered by Vestige, Built by evilcorp.algo"
        )
        attachments.append(discord.File(fp="./images/logo.png", filename="vestige.png"))

        view = TickerView(interaction, currencies, currency, token, 120)

        await interaction.edit_original_response(embed=embed, attachments=attachments, view=view) 
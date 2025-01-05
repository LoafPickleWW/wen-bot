from src.Bot import Bot
from src.ticker.utils import load_ticker_data

async def load_the_bot(bot: Bot):
    await load_ticker_data(bot)
    
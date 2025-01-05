import aiohttp, asyncio, aiofiles, io
import pandas as pd

from src.Bot import Bot
from src.ticker.TokenInfo import TokenInfo
from consts import NETWORK_ID, HEADERS, SEARCH_URL, TICKER_DATA_PATH

from src.logger import notify_bot

async def get_ticker_candles(interaction, asset_id, interval, start):
    url = (f"https://indexer.vestige.fi/assets/{asset_id}/candles?"
           f"network_id={NETWORK_ID}&interval={interval}&start={start}"
           f"&denominating_asset_id=0&volume_in_denominating_asset=false")
    
    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    session = aiohttp.ClientSession(connector=conn)
    async with session.get(url=url, headers=HEADERS) as response:
        if response.status == 200:
            candles = await response.json()
        else:
            notify_bot(interaction, f"error processing candles :: {response}")
            await session.close()
            return None
    await session.close()  

    if not candles: return None
    
    return candles

async def get_ticker_info(interaction, bot, ticker):
    
    tmp_ticker = ticker
    if tmp_ticker in bot.ticker_data:
        tmp_ticker = bot.ticker_data[ticker]

    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    session = aiohttp.ClientSession(connector=conn)
    async with session.get(url=SEARCH_URL.format(tmp_ticker), headers=HEADERS) as response:
        if response.status == 200:
            data = await response.json()
        else:
            notify_bot(interaction, f"error processing ticker :: {response}")
            await session.close()
            return None
    await session.close()  

    tokens = []
    # Exact Match
    for token in data:
        token_info = TokenInfo(token)
        if ticker.lower() == token_info.ticker.lower().strip():
            tokens.append(token_info)
    # Close enough
    if len(tokens) <= 0:
        for token in data:
            token_info = TokenInfo(token)
            if ticker.lower() in token_info.ticker.lower():
                tokens.append(token_info)
    # Highest liquidity wins
    if tokens:
        highest_liquidity_token = max(tokens, key=lambda x: x.liquidity)
        return highest_liquidity_token
    else:
        return None
    
async def load_ticker_data(bot: Bot):
    try:
        loop = asyncio.get_running_loop()
        async with aiofiles.open(TICKER_DATA_PATH, mode='r') as file:
            content = await file.read()
        user_df = await loop.run_in_executor(None, lambda: pd.read_csv(io.StringIO(content), dtype=object))
        
        for _, row in user_df.iterrows():
            bot.ticker_data[row["ticker"]] = str(row["asset_id"])
    except Exception as e:
        print(f"ERROR: loading ticker data: {e}")
        bot.user_data = {}

def find_highest_and_lowest(candles):
    highest_high = max(item["high"] for item in candles)
    lowest_low = min(item["low"] for item in candles)
    return highest_high, lowest_low

def calculate_percentage_change(current_price, price_24hr_ago, price_7days_ago):
    def percentage_change(new_price, old_price):
        if old_price == 0:
            return None
        return ((new_price - old_price) / old_price) * 100

    change_24hr = percentage_change(current_price, price_24hr_ago)
    change_7days = percentage_change(current_price, price_7days_ago)
    return change_24hr, change_7days

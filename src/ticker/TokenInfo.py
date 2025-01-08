class TokenInfo:
    def __init__(self, json_object):
            self.image = json_object["image"]
            self.asset_id = json_object["id"]
            self.asset_name = json_object["name"]
            self.ticker = json_object["ticker"]

            self.creation_timestamp = json_object["created_at"]
            self.decimals = json_object["decimals"]
            
            self.total_lockup = json_object["total_lockup"]
            self.rank = json_object["rank"]
            self.tvl = json_object["tvl"]
            self.market_cap = json_object["market_cap"]

            self.price = json_object["price"]
            self.price1h = json_object["price1h"]
            self.price1d = json_object["price1d"]
            self.price7d = json_object["price7d"]

            self.volume1h = json_object["volume1h"]
            self.volume1d = json_object["volume1d"]
            self.volume7d = json_object["volume7d"]

            self.swaps1h = json_object["swaps1h"]
            self.swaps1d = json_object["swaps1d"]
            self.swaps7d = json_object["swaps7d"]

            # Calculated items
            self.graph = None
            
            self.highest_24h = None
            self.lowest_24h = None
            
            self.highest_7d = None
            self.lowest_7d = None

            self.change_24_hrs = None
            self.change_7_days = None
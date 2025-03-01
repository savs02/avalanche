import json
def generate_prompt(trades, past_trades):
    prompt = "You are a crypto trading assistant analyzing multiple coins.\n\n"
    
    for trade in trades:
        coin_id = trade["id"]
        name = trade["name"]
        price = trade["price"]
        price_change = trade["price_change_percentage_24h"]
        volume = trade["total_volume"]
        market_cap = trade["market_cap"]

        past_trade_data = json.dumps(past_trades.get(coin_id, []), indent=4)

        prompt += f"""
        Coin: {name}
        - Current Price: ${price}
        - 24h Price Change: {price_change}%
        - Market Cap: {market_cap}
        - Trading Volume: {volume}

        Past Trades for {name}:
        {past_trade_data}

        Analyze the trends and provide insights:
        1. What strategy should the user consider for {name} based on past trades and current market conditions? Provide a risk assessment. 
        2. Compare current market trends for {name} to past successful trades made by the user. Identify similarities if any.
        3. Highlight any patterns or trading windows where {name} performs best (e.g., time of day, volume spikes).
        4. If the user has attached a specific question, answer it directly with a clear recommendation.  
        """
    
    return prompt


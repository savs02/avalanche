import os
import json
import datetime
import requests
from dotenv import load_dotenv
from data_retrieval import CoinData
from previous_trades import PreviousTrades
from openai import OpenAI
from crypto_news import CryptoNews  # Import the CryptoNews class

load_dotenv()

# Initialize APIs and data.
API_KEY = os.getenv("OPENAI_API_KEY")
data = json.loads(CoinData().get_data())
client = OpenAI(api_key=API_KEY)
trades = PreviousTrades(openai_api_key=API_KEY)
crypto_news = CryptoNews()  # Initialize your CryptoNews instance

# Get coin name dynamically from the user.
coin_name = input("Enter the coin name (e.g., 'ethereum'): ")

# Define the tools with the new get_context tool added.
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "Get the current price for the given coin. Accepts a coin id (e.g., 'bitcoin') as a string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string"}
                },
                "required": ["coin"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_trend",
            "description": (
                "Retrieve the historical data for the given coin so that the model can analyze "
                "and determine the trend based on its reasoning."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string"}
                },
                "required": ["coin"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_trends",
            "description": (
                "Compare the historical data for all the coins and provide an analysis of their trends."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_summary",
            "description": "Provide a brief summary of the market conditions based on available data."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_trade",
            "description": (
                "Make a trade for the given coin. Accepts a coin id (e.g., 'bitcoin') as a string."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string"}
                },
                "required": ["coin"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "give_advice",
            "description": (
                "Advice the user on making a trade based on previous trades and comparison with their trends so far."
            ),
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_crypto_news",
            "description": "Retrieve the latest cryptocurrency news articles from sources."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "End the chat."
        }
    }
]

# Build the user messages.
messages = [
    {"role": "user", "content": f"Give me advice depending on what's happened so far in the markets."},
    {"role": "user", "content": f"Make a trade for {coin_name}"},
    {"role": "user", "content": "Give me the latest summary of what's happened so far in the markets."},
    {"role": "user", "content": "Based on historical data, what trend do you see for all the coins?"},
    {"role": "user", "content": f"What's the current price for {coin_name}?"},
    {"role": "user", "content": f"What trend do you see for {coin_name}?"},
    {"role": "user", "content": "Show me the latest crypto news context."},  # Triggers the get_context tool.
    {"role": "user", "content": f"Bye. End the chat."},
]

# Call the model with the user messages and the defined tools.
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
)

# Retrieve the assistant message (which contains the tool_calls).
assistant_message = completion.choices[0].message
tool_calls = assistant_message.tool_calls

# Append the assistant message to the conversation.
messages.append(assistant_message)

# Define the functions.
def get_price(coin: str):
    if coin in data:
        coin_data = data[coin]
        price = coin_data.get("market data", {}).get("current_price", "Price not available")
        return f"The current price for {coin} is {price}."
    else:
        return f"Data for {coin} not found."

def get_trend(coin: str):
    if coin in data:
        coin_data = data[coin]
        historical_data = coin_data.get("historical data")
        if historical_data is not None:
            prices = historical_data["prices"]
            market_caps = historical_data["market_caps"]
            total_volumes = historical_data["total_volumes"]
            trend = (1/3) * (
                ((prices[2][1] - prices[0][1]) / prices[0][1]) +
                ((market_caps[2][1] - market_caps[0][1]) / market_caps[0][1]) +
                ((total_volumes[2][1] - total_volumes[0][1]) / total_volumes[0][1])
            )
            if trend > 0:
                return "positive trend based on historical data analysed"
            elif trend < 0:
                return "negative trend based on historical data analysed"
            else:
                return "stagnant based on historical data analysed"
        else:
            return f"No historical data available for {coin}."
    else:
        return f"Data for {coin} not found."

def compare_trends():
    analysis = []
    for coin, coin_data in data.items():
        historical_data = coin_data.get("historical data")
        if historical_data:
            prices = historical_data.get("prices", [])
            market_caps = historical_data.get("market_caps", [])
            total_volumes = historical_data.get("total_volumes", [])
            if len(prices) >= 3 and len(market_caps) >= 3 and len(total_volumes) >= 3:
                trend = (1/3) * (
                    ((prices[2][1] - prices[0][1]) / prices[0][1]) +
                    ((market_caps[2][1] - market_caps[0][1]) / market_caps[0][1]) +
                    ((total_volumes[2][1] - total_volumes[0][1]) / total_volumes[0][1])
                )
                analysis.append((coin, trend))
    if not analysis:
        return "No sufficient historical data available for comparison."
    analysis.sort(key=lambda x: x[1])
    worst = analysis[0]
    best = analysis[-1]
    return (
        f"Out of {len(analysis)} coins analyzed, {best[0]} shows the strongest upward trend "
        f"(trend index = {best[1]:.2f}) and {worst[0]} shows the strongest downward trend "
        f"(trend index = {worst[1]:.2f})."
    )

def get_summary():
    """
    Compute a three-line morning digest summary:
        1. Market prices summary (range and average).
        2. Notable trend analysis from all coins.
        3. A concluding digest line.
    """
    coin_prices = []
    trend_results = []
    
    for coin, coin_data in data.items():
        current_price = coin_data.get("market data", {}).get("current_price")
        if current_price is not None:
            try:
                coin_prices.append(float(current_price))
            except Exception:
                pass
        
        historical_data = coin_data.get("historical data")
        if historical_data:
            prices = historical_data.get("prices", [])
            market_caps = historical_data.get("market_caps", [])
            total_volumes = historical_data.get("total_volumes", [])
            if len(prices) >= 3 and len(market_caps) >= 3 and len(total_volumes) >= 3:
                trend = (1/3) * (
                    ((prices[2][1] - prices[0][1]) / prices[0][1]) +
                    ((market_caps[2][1] - market_caps[0][1]) / market_caps[0][1]) +
                    ((total_volumes[2][1] - total_volumes[0][1]) / total_volumes[0][1])
                )
                trend_results.append((coin, trend))
    
    summary_lines = []
    if coin_prices:
        min_price = min(coin_prices)
        max_price = max(coin_prices)
        avg_price = sum(coin_prices) / len(coin_prices)
        summary_lines.append(f"Market prices range from ${min_price:.2f} to ${max_price:.2f}, with an average of ${avg_price:.2f}.")
    else:
        summary_lines.append("No price data available.")
    
    if trend_results:
        trend_results.sort(key=lambda x: x[1])
        worst_coin, worst_trend = trend_results[0]
        best_coin, best_trend = trend_results[-1]
        summary_lines.append(f"{best_coin} is leading upward (trend index = {best_trend:.2f}), while {worst_coin} is lagging (trend index = {worst_trend:.2f}).")
    else:
        summary_lines.append("No trend data available.")
    
    summary_lines.append("This is your morning market digest.")
    
    return "\n".join(summary_lines)

def make_trade(coin: str):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if coin in data:
        coin_data = data[coin]
        price = coin_data.get("market data", {}).get("current_price", "Price not available")
        trades.add_trade(messages[1]["content"], coin, price, current_time)
        return f"Trade for {coin} at {price} has been successfully made at {current_time}."
    return f"{coin} not found."

def give_advice():
    trend_analysis = compare_trends()
    prev_trades = trades.get_trade(messages[0]["content"])
    if "strongest upward trend" in trend_analysis and "strongest downward trend" in trend_analysis:
        upward_coin = trend_analysis.split("strongest upward trend")[1].split("and")[0].strip()
        downward_coin = trend_analysis.split("strongest downward trend")[1].strip()
        if prev_trades:
            advice = f"Based on historical trends, {upward_coin} shows a strong upward trend, while {downward_coin} is on a downward trajectory. "
            advice += "Since you've previously traded these, it might be wise to consider holding or selling {downward_coin}, and buying {upward_coin} if you haven't already done so."
        else:
            advice = f"Based on historical trends, {upward_coin} shows a strong upward trend, while {downward_coin} is on a downward trajectory. "
            advice += "Consider buying {upward_coin} to capitalize on the trend."
    else:
        advice = "Insufficient data to provide an analysis of trends or previous trades."
    return advice

def get_crypto_news():
    news, output_string_arr = crypto_news.get_crypto()
    return "\n".join(output_string_arr)

def finish():
    return "Thank you for using the crypto trading assistant. Have a nice day!"

# Process each tool call and append a corresponding tool message.
for tool_call in tool_calls:
    if tool_call.function.name == "give_advice":
        result = give_advice()
    elif tool_call.function.name == "compare_trends":
        result = compare_trends()
    elif tool_call.function.name == "get_summary":
        result = get_summary()
    elif tool_call.function.name == "get_crypto_news":
        result = get_crypto_news()
    else:
        args = json.loads(tool_call.function.arguments)
        if tool_call.function.name == "get_price":
            result = get_price(args["coin"])
        elif tool_call.function.name == "get_trend":
            result = get_trend(args["coin"])
        elif tool_call.function.name == "make_trade":
            result = make_trade(args["coin"])
        else:
            result = "No matching function found."
    
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

# Add an extra instruction for the model.
messages.append({
    "role": "user",
    "content": "Based on the provided data and analysis, please summarize the overall trends among the coins."
})

# Final API call with the updated conversation.
completion_2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
)

print(completion_2.choices[0].message.content)
import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from dotenv import load_dotenv
from data_retrieval import CoinData
from previous_trades import PreviousTrades
# from openai import OpenAI
from crypto_news import CryptoNews 
from datetime import datetime

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PORT = int(os.getenv('PORT', 5050))



########## Define tooling
# def get_weather(location: str):
#     # Example logic to get weather information
#     # You can make an API call to a weather service, like OpenWeatherMap
#     weather = f"The current temperature in {location} is 22°C."  # Placeholder response
#     return weather


# tools = [{
#         "type": "function",
#         "name": "get_weather",
#         "description": "Get current temperature for a given location.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "City and country e.g. Bogotá, Colombia"
#                 }
#             },
#             "required": [
#                 "location"
#             ],
#             "additionalProperties": False
#         }
#     }
# ]


# available_functions = {
#     "get_weather": get_weather
# }


tools = [
    {
        "type": "function",
        "name": "get_price",
        "description": "Get the current price for the given coin. Accepts a coin id (e.g., 'bitcoin') as a string. Options coins are: bitcoin, ethereum, ripple. If another coin is mentioned, say that this is not currently supported.",
        "parameters": {
            "type": "object",
            "properties": {
                "coin": {"type": "string"}
            },
            "required": ["coin"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "get_trend",
        "description": (
            "Retrieve the historical data for the given coin so that the model can analyze "
            "and determine the trend based on its reasoning. Mention that the historical data is over the last 3 days. "
            "Explain any fluctuations and changes as well as the overall general trend, referencing specific values. Be detailed in your response and mention specific value.  Make sure to ennunciate positive and negative trend indexes e.g., '-0.18' as 'negative 0.18'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "coin": {"type": "string"}
            },
            "required": ["coin"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "compare_trends",
        "description": (
            "Compare the historical data for all the coins and provide an analysis of their trends. Be detailed in your response. "
            "Mention that the historical data is over the last 3 days. Consider all pairings of the coins and comparisons. Conclude with a 1-line summary of the findings. "
            "Mention specfific values to back up your assessments and be detailed. Make sure to ennunciate positive and negative trend indexes e.g., '-0.18' as 'negative 0.18'."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "get_summary",
        "description": "Provide a brief summary of the market conditions based on available data.  Make sure to ennunciate positive and negative trend indexes e.g., '-0.18' as 'negative 0.18'.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    # {
    #     "type": "function",
    #     "name": "make_trade",
    #     "description": (
    #         "Make a trade for the given coin. Accepts a coin id (e.g., 'bitcoin') as a string."
    #     ),
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "coin": {"type": "string"}
    #         },
    #         "required": ["coin"],
    #         "additionalProperties": False
    #     }
    # } #,
    # {
    #     "type": "function",
    #     "name": "give_advice",
    #     "description": (
    #         "Advice the user on making a trade based on previous trades and comparison with their trends so far."
    #     )
    # },
    {
        "type": "function",
        "name": "get_crypto_news",
        "description": "Retrieve the latest cryptocurrency news articles from sources. Be detailed in your response, mentioning the titles of the news articles and then explaining the findings. Add specfific coin values.  Make sure to ennunciate positive and negative trend indexes e.g., '-0.18' as 'negative 0.18'.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "finish",
        "description": "End the chat.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
]


data = CoinData().get_data()
data_dict = json.loads(data)
trades = PreviousTrades(openai_api_key=OPENAI_API_KEY)
crypto_news = CryptoNews()

# messages = [
#     {"role": "user", "content": f"Give me advice depending on what's happened so far in the markets."},
#     {"role": "user", "content": f"Make a trade for {coin_name}"},
#     {"role": "user", "content": "Give me the latest summary of what's happened so far in the markets."},
#     {"role": "user", "content": "Based on historical data, what trend do you see for all the coins?"},
#     {"role": "user", "content": f"What's the current price for {coin_name}?"},
#     {"role": "user", "content": f"What trend do you see for {coin_name}?"},
#     {"role": "user", "content": "Show me the latest crypto news context."}  # Triggers the get_context tool.
# ]

def get_price(coin: str):
    if coin in data_dict:
        coin_data = data_dict[coin]
        price = coin_data.get("market data", {}).get("current_price", "Price not available")
        return f"The current price for {coin} is {price}."
    else:
        return f"Data for {coin} not found."

def get_trend(coin: str):
    if coin in data_dict:
        coin_data = data_dict[coin]
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
    for coin, coin_data in data_dict.items():
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
    
    for coin, coin_data in data_dict.items():
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
    data_dict = json.loads(data)
    if coin in data_dict:
        coin_data = data_dict[coin]
        price = coin_data.get("market data", {}).get("current_price", "Price not available")
        # trades.add_trade(messages[1]["content"], coin, price, current_time)
        trades.add_trade(messages[1]["content"], coin, price, current_time)
        return f"Trade for {coin} at {price} has been successfully made at {current_time}."
    return f"{coin} not found."

# def give_advice():
#     analysis_trends = compare_trends()
#     prev_trades = trades.get_trade(messages[0]["content"])
#     if "strongest upward trend" in analysis_trends and "strongest downward trend" in analysis_trends:
#         upward_coin = analysis_trends.split("strongest upward trend")[1].split("and")[0].strip()
#         downward_coin = analysis_trends.split("strongest downward trend")[1].strip()
#         if prev_trades:
#             advice = f"Based on historical trends, {upward_coin} shows a strong upward trend, while {downward_coin} is on a downward trajectory. "
#             advice += "Since you've previously traded these, it might be wise to consider holding or selling {downward_coin}, and buying {upward_coin} if you haven't already done so."
#         else:
#             advice = f"Based on historical trends, {upward_coin} shows a strong upward trend, while {downward_coin} is on a downward trajectory. "
#             advice += "Consider buying {upward_coin} to capitalize on the trend."
#     else:
#         advice = "Insufficient data to provide an analysis of trends or previous trades."
#     return advice


def get_crypto_news():
    news, output_string_arr = crypto_news.get_crypto()
    return "\n".join(output_string_arr)

def finish():
    return "Thank you for using the crypto trading assistant. Have a nice day!"


available_functions = {
    # "give_advice": give_advice,
    "compare_trends": compare_trends,
    "get_summary": get_summary,
    "get_crypto_news": get_crypto_news,
    "get_price": get_price,
    "get_trend": get_trend,
    # "make_trade": make_trade #,
    "finish": finish
}



########## Start Twilio and OpenAI integration

SYSTEM_MESSAGE = (
    # "You are a concise and knowledgeable crypto trading assistant. Keep responses under 100 words while delivering precise market insights. Stay professional but approachable, offering facts, trends, and news. Keep jokes minimal, but if appropriate, a subtle reference to market volatility or a light trading pun is welcome."
    "You are a concise and knowledgeable crypto trading assistant. Deliver precise market insights. Stay professional but approachable, offering facts, trends, and news. Keep jokes minimal, but if appropriate, a subtle reference to market volatility or a light trading pun is welcome."
)
VOICE = 'alloy'
LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created'
]
SHOW_TIMING_MATH = False

app = FastAPI()

if not OPENAI_API_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response to connect to Media Stream."""
    response = VoiceResponse()
    # <Say> punctuation to improve text-to-speech flow
    response.say("Please wait while we connect your call to the A.I. crypto trading assistant developed by Team Avalanche.")
    response.pause(length=1)
    response.say("O.K. you can start talking!")
    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")

@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections between Twilio and OpenAI."""
    print("Client connected")
    await websocket.accept()

    async with websockets.connect(
        'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as openai_ws:
        await initialize_session(openai_ws)

        # Connection specific state
        stream_sid = None
        latest_media_timestamp = 0
        last_assistant_item = None
        mark_queue = []
        response_start_timestamp_twilio = None
        
        async def receive_from_twilio():
            """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
            nonlocal stream_sid, latest_media_timestamp
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)
                    if data['event'] == 'media' and openai_ws.open:
                        latest_media_timestamp = int(data['media']['timestamp'])
                        audio_append = {
                            "type": "input_audio_buffer.append",
                            "audio": data['media']['payload']
                        }
                        await openai_ws.send(json.dumps(audio_append))
                    elif data['event'] == 'start':
                        stream_sid = data['start']['streamSid']
                        print(f"Incoming stream has started {stream_sid}")
                        response_start_timestamp_twilio = None
                        latest_media_timestamp = 0
                        last_assistant_item = None
                    elif data['event'] == 'mark':
                        if mark_queue:
                            mark_queue.pop(0)
            except WebSocketDisconnect:
                print("Client disconnected.")
                if openai_ws.open:
                    await openai_ws.close()
        
        async def send_weather_info_to_twilio(weather_info: str):
            weather_audio = base64.b64encode(weather_info.encode('utf-8')).decode('utf-8')
            audio_response = {
                "event": "media",
                "streamSid": stream_sid,
                "media": {
                    "payload": weather_audio
                }
            }
            await websocket.send_json(audio_response)


        async def send_to_twilio():
            """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
            nonlocal stream_sid, last_assistant_item, response_start_timestamp_twilio
            try:
                async for openai_message in openai_ws:
                    response = json.loads(openai_message)
                    if response['type'] in LOG_EVENT_TYPES:
                        print(f"Received event: {response['type']}", response)

                    if response.get('type') == 'response.audio.delta' and 'delta' in response:
                        audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                        audio_delta = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {
                                "payload": audio_payload
                            }
                        }
                        await websocket.send_json(audio_delta)

                        if response_start_timestamp_twilio is None:
                            response_start_timestamp_twilio = latest_media_timestamp
                            if SHOW_TIMING_MATH:
                                print(f"Setting start timestamp for new response: {response_start_timestamp_twilio}ms")

                    # Update last_assistant_item safely
                    if response.get('item_id'):
                        last_assistant_item = response['item_id']
                        

                    if response.get('type') == 'response.done':
                        print("RESPONSE TYPE IS DONE")
                        
                        items = response["response"]["output"]

                        print("ITEMS: ", items)

                        for item in items:
                            if item.get("type") == "function_call":
                                print("FOUND FUNCTION CALL")
                                function_name = item.get("name")
                                function_args = json.loads(item.get("arguments"))

                                function_to_call = available_functions[function_name]
                                try:
                                    function_response = function_to_call(**function_args)
                                    # function_response = get_weather(**function_args)
                                    print("FUNCTION CALL RESPONSE: ", function_response)
                                except Exception as e:
                                    print(f"Error calling function {item['name']}: {e}")

                                # Send function output to OpenAI WebSocket
                                try:
                                    await openai_ws.send(json.dumps({
                                        "type": "conversation.item.create",
                                        "item": {
                                            "type": "function_call_output",
                                            "call_id": item.get("call_id"),
                                            "output": function_response
                                        }
                                    }))
                                except Exception as e:
                                    print(f"Error sending function output to OpenAI: {e}")

                                # Define a valid response trigger
                                response_create = {
                                    "type": "response.create"
                                }
                                await openai_ws.send(json.dumps(response_create))

                    # Trigger an interruption. Your use case might work better using `input_audio_buffer.speech_stopped`, or combining the two.
                    if response.get('type') == 'input_audio_buffer.speech_started':
                        print("Speech started detected.")
                        if last_assistant_item:
                            print(f"Interrupting response with id: {last_assistant_item}")
                            await handle_speech_started_event()
            except Exception as e:
                print(f"Error in send_to_twilio: {e}")

        async def handle_speech_started_event():
            """Handle interruption when the caller's speech starts."""
            nonlocal response_start_timestamp_twilio, last_assistant_item
            print("Handling speech started event.")
            if mark_queue and response_start_timestamp_twilio is not None:
                elapsed_time = latest_media_timestamp - response_start_timestamp_twilio
                if SHOW_TIMING_MATH:
                    print(f"Calculating elapsed time for truncation: {latest_media_timestamp} - {response_start_timestamp_twilio} = {elapsed_time}ms")

                if last_assistant_item:
                    if SHOW_TIMING_MATH:
                        print(f"Truncating item with ID: {last_assistant_item}, Truncated at: {elapsed_time}ms")

                    truncate_event = {
                        "type": "conversation.item.truncate",
                        "item_id": last_assistant_item,
                        "content_index": 0,
                        "audio_end_ms": elapsed_time
                    }
                    await openai_ws.send(json.dumps(truncate_event))

                await websocket.send_json({
                    "event": "clear",
                    "streamSid": stream_sid
                })

                mark_queue.clear()
                last_assistant_item = None
                response_start_timestamp_twilio = None

        async def send_mark(connection, stream_sid):
            if stream_sid:
                mark_event = {
                    "event": "mark",
                    "streamSid": stream_sid,
                    "mark": {"name": "responsePart"}
                }
                await connection.send_json(mark_event)
                mark_queue.append('responsePart')

        await asyncio.gather(receive_from_twilio(), send_to_twilio())

async def send_initial_conversation_item(openai_ws):
    """Send initial conversation item if AI talks first."""
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Greet the user with 'Hello there! I am Ava, an AI crypto trading assistant! You can ask me for a summary of the current market conditions or the latest news, give feedback on a coin, compare trends amongst coins. How can I help you?'"
                }
            ]
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))


async def initialize_session(openai_ws):
    """Control initial session with OpenAI."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
            "tools": tools,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))

    # Uncomment the next line to have the AI speak first
    # await send_initial_conversation_item(openai_ws)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
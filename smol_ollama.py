from smolagents import CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool, LiteLLMModel, PythonInterpreterTool, tool
from typing import Optional
import requests
# model = LiteLLMModel(model_id="ollama/qwen2.5-coder:7b")

model = LiteLLMModel(
    model_id="ollama_chat/llama3.2:latest",
    api_base="http://localhost:11434",  # Adjust if using a remote server
    #api_key="openai_should_release_more_open_models"  # Replace with your API key if required
)

#@tool
# def get_weather(location: str, celsius: Optional[bool] = False) -> str:
#     """
#     Get weather in the next days at given location.
#     Args:
#         location: the location
#         celsius: whether to use Celsius for temperature
#     """
#     #return f"The weather in {location} is sunny with temperatures around 25°C."
#     return f"The weather in {location} is not found."

@tool
def get_weather(location: str, celsius: Optional[bool] = True) -> str:
    """
    Get weather in the next days at a given location using Open-Meteo API.
    Args:
        location: the location
        celsius: whether to use Celsius for temperature
    """
    # Geocoding API for latitude/longitude (can use Open-Meteo or a free geocoding service)
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    try:
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()
        if not geocode_data.get("results"):
            return f"Could not find the location: {location}."
        
        lat = geocode_data["results"][0]["latitude"]
        lon = geocode_data["results"][0]["longitude"]

        # Open-Meteo API for weather
        units = "metric" if celsius else "imperial"
        weather_url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "temperature_unit": "celsius" if celsius else "fahrenheit",
        }

        weather_response = requests.get(weather_url, params=params)
        weather_data = weather_response.json()

        if "current_weather" in weather_data:
            temperature = weather_data["current_weather"]["temperature"]
            windspeed = weather_data["current_weather"]["windspeed"]
            return (f"The current weather in {location} is {temperature}°{'C' if celsius else 'F'} "
                    f"with a wind speed of {windspeed} km/h.")
        else:
            return "Weather data is not available right now."
    except Exception as e:
        return f"An error occurred: {e}"


#agent = ToolCallingAgent(tools=[get_weather], model=model)


#agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model, additional_authorized_imports=["requests", "re"])

#answer = agent.run("What is the weather in Hyderabad today?")
#print(answer)




# Initialize the agent
agent = ToolCallingAgent(tools=[get_weather], model=model)

# Query the weather
answer = agent.run("What is the weather in Hyderabad today in Celsius?")
print(answer)
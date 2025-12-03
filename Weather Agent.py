import requests

# Set your OpenWeatherMap API key here
OPENWEATHER_API_KEY = "689de3ceb70edd29fd1ffd01adec3f5c"

class WeatherAgent:
    def init(self, api_key):
        self.api_key = api_key
    
    def get_weather(self, city_name):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        return response.json()
    
    def parse_weather_info(self, weather_data, days):
        temperatures = []
        probabilities = []

        for forecast in weather_data['list'][:days]:  # Get the next 'days' weather forecasts
            temperature = forecast['main']['temp']
            rain = forecast.get('rain', {}).get('3h', 0)  # Get the rain volume for the next 3 hours, if available
            temperatures.append(f"{temperature}°C")
            probabilities.append(f"{rain}%")

        return temperatures, probabilities
    
    def format_weather_info(self, city_name, temperatures, probabilities, days):
        formatted_info = f"Weather forecast for {city_name} for the next {days} days:\n"
        for i in range(days):
            formatted_info += f"Day {i+1}: Temperature: {temperatures[i]}, Rainfall Probability: {probabilities[i]}\n"
        return formatted_info
    
    def run(self):
        user_input = input("Enter city name and number of days (e.g., 'Nalgonda 3'): ")
        parts = user_input.split()
        city_name = " ".join(parts[:-1])
        days = int(parts[-1])

        weather_data = self.get_weather(city_name)
        temperatures, probabilities = self.parse_weather_info(weather_data, days)
        formatted_info = self.format_weather_info(city_name, temperatures, probabilities, days)

        print(formatted_info)

# Example usage
weather_agent = WeatherAgent(OPENWEATHER_API_KEY)
weather_agent.run() 

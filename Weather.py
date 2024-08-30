import tkinter as tk
from tkinter import messagebox
import requests
import json
from PIL import Image, ImageTk


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("700x500")

        #  background image
        self.bg_image = ImageTk.PhotoImage(Image.open("img.png"))
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.location_label = tk.Label(root, text="Enter a city or PIN code:", font=("Arial", 14), fg="white",
                                       bg="#333")
        self.location_label.pack(pady=20)
        self.location_entry = tk.Entry(root, width=30, font=("Arial", 14))
        self.location_entry.pack()

        self.get_weather_button = tk.Button(root, text="Get Weather", command=self.get_weather, font=("Arial", 14),
                                            fg="white", bg="#4CAF50")
        self.get_weather_button.pack(pady=10)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_input, font=("Arial", 14), fg="white",
                                      bg="#FF9800")
        self.clear_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.root.destroy, font=("Arial", 14), fg="white",
                                     bg="#FF0000")
        self.exit_button.pack(pady=10)

        self.temperature_label = tk.Label(root, text="", font=("Arial", 18), fg="white", bg="#333")
        self.temperature_label.pack(pady=20)
        self.humidity_label = tk.Label(root, text="", font=("Arial", 18), fg="white", bg="#333")
        self.humidity_label.pack(pady=20)
        self.weather_conditions_label = tk.Label(root, text="", font=("Arial", 18), fg="white", bg="#333")
        self.weather_conditions_label.pack(pady=20)

    def clear_input(self):
        self.location_entry.delete(0, tk.END)
        self.temperature_label.config(text="")
        self.humidity_label.config(text="")
        self.weather_conditions_label.config(text="")

    def get_weather(self):
        location = self.location_entry.get()
        api_key = "Add your OpenWeatherMap API key"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        try:
            response = requests.get(base_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve weather data: {e}")
            return

        try:
            weather_data = json.loads(response.text)
            temperature_kelvin = weather_data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            humidity = weather_data['main']['humidity']
            weather_conditions = weather_data['weather'][0]['description']

            self.temperature_label.config(text=f"Temperature: {temperature_celsius:.2f}°C")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.weather_conditions_label.config(text=f"Weather Conditions: {weather_conditions}")
        except (KeyError, IndexError) as e:
            messagebox.showerror("Error", f"Failed to parse weather data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

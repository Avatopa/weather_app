import requests
import tkinter as tk
from PIL import Image, ImageTk
import json

API_KEY = "ee21c2594ee1df3a3fb863fa71eb7cab"

window = tk.Tk()
window.title("Weather App")
window.geometry("800x600")

# ---------- background ----------

bg_image = Image.open("rain.png")
bg_image = bg_image.resize((800,600))

bg_photo = ImageTk.PhotoImage(bg_image)

background = tk.Label(
    window,
    image=bg_photo
)

background.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

weather_photo = None
frames = []
# ---------- gif ----------

def play_gif(i=0):

    if len(frames) > 0:

        weather_icon.config(
            image=frames[i]
        )

        window.after(
            150,
            play_gif,
            (i + 1) % len(frames)
        )

# ---------- change image ----------

def change_weather_image(condition):

    global weather_photo, frames

    condition = condition.lower()

    if "rain" in condition:
        image_file = "images/rain.png"
        gif_file = "images/rain.gif"


    elif "cloud" in condition:
        image_file = "images/cloud.png"
        gif_file = "images/rain.gif"


    elif "clear" in condition:
        image_file = "images/clear.png"
        gif_file = "images/rain.gif"


    elif "snow" in condition:
        image_file = "images/snow.png"
        gif_file = "images/rain.gif"


    else:
        image_file = "images/cloud.png"
        gif_file = "images/rain.gif"

    # عکس ثابت

    img = Image.open(image_file)
    img = img.resize((200,200))

    weather_photo = ImageTk.PhotoImage(img)

    weather_icon.config(
        image=weather_photo
    )
    
    # GIF

    gif = Image.open(gif_file)

    frames = []

    for i in range(gif.n_frames):

        gif.seek(i)

        frames.append(
            ImageTk.PhotoImage(
                gif.copy()
            )
        )

    play_gif()
# ---------- API ----------

def get_weather():

    city = entry.get()

    if not city:
        result.set("اسم شهر رو وارد کن")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {

        "q": city,

        "appid": API_KEY,

        "units": "metric"

    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    if data.get("cod") == 200:

        condition = data["weather"][0]["main"]

        result.set(
            f"🌍 City: {data['name']}\n"
            f"🌡 Temp: {data['main']['temp']} °C\n"
            f"🌥 {condition}\n"
            f"💨 Wind: {data['wind']['speed']} m/s"
        )

        change_weather_image(condition)

        with open(
            "weather.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    else:

        result.set(
            "City not found"
        )
# ---------- UI ----------
frame = tk.Frame(
    window,
    bg="black"
)

frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

entry = tk.Entry(
    frame,
    font=("Arial",20),
    width=20
)

entry.pack(pady=10)

button = tk.Button(
    frame,
    text="Get Weather",
    command=get_weather,
    font=("Arial",16)
)

button.pack()

result = tk.StringVar()

label = tk.Label(
    frame,
    textvariable=result,
    font=("Arial",16),
    bg="black",
    fg="white"
)

label.pack(pady=20)

weather_icon = tk.Label(
    frame,
    bg="black"
)
weather_icon.pack()

window.mainloop()
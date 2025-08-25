import os, re, json, time, random, datetime as dt
import requests

BOT_NAME = "Tazahnae's Bot 🤖"
HISTORY_FILE = "history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

def help_text():
    return (
        f"{BOT_NAME} commands:\n"
        "  - hello / hi\n"
        "  - time / date\n"
        "  - joke\n"
        "  - weather <city>\n"
        "  - remember <note>\n"
        "  - notes\n"
        "  - clear notes\n"
        "  - math: <expr>   (e.g., math: 12*(3+4))\n"
        "  - help\n"
        "  - exit / quit (CLI)\n"
    )

def tell_joke():
    try:
        r = requests.get(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json"},
            timeout=6,
        )
        if r.ok:
            return r.json().get("joke", "Couldn't fetch a joke right now.")
        return "Couldn't fetch a joke right now."
    except Exception:
        return "Hmm, the joke pipes are clogged. Try again."

def current_time():
    now = dt.datetime.now()
    return now.strftime("It's %I:%M %p on %A, %B %d, %Y.")

def eval_math(expr):
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
        return "I only support basic math (digits and + - * / ( ))."
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception:
        return "That math expression seems off."

def weather_for(city):
    key = os.getenv("OPENWEATHER_API_KEY")
    if key:
        # Use OpenWeather if key is set
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": key, "units": "imperial"}
            r = requests.get(url, params=params, timeout=8)
            if r.status_code == 404:
                return f"Couldn't find weather for '{city}'."
            r.raise_for_status()
            data = r.json()
            desc = data["weather"][0]["description"].title()
            temp = round(data["main"]["temp"])
            feels = round(data["main"]["feels_like"])
            city_name = data["name"]
            return f"{city_name}: {desc}, {temp}°F (feels {feels}°F)."
        except Exception as e:
            return f"Weather error (OpenWeather): {e}"
    else:
        # Fallback: wttr.in (no API key needed)
        try:
            url = f"https://wttr.in/{city}?format=3"
            r = requests.get(url, timeout=6)
            r.raise_for_status()
            return r.text.strip() or f"Couldn't get weather for '{city}'."
        except Exception as e:
            return f"Weather error (fallback): {e}"

def respond(user_input: str):
    history = load_history()
    notes = [h["text"] for h in history if h.get("type") == "note"]

    text = (user_input or "").strip()
    low = text.lower()

    if low in {"help", "/help"}:
        return help_text()
    if low in {"time", "date"}:
        return current_time()
    if low in {"hello", "hi", "hey"}:
        return random.choice(["Hey!", "Hi there!", "What's up!"])
    if low == "joke":
        return tell_joke()
    if low.startswith("math:"):
        expr = text[5:].strip()
        return eval_math(expr)
    if low.startswith("remember "):
        note = text[9:].strip()
        if note:
            notes.append(note)
            history.append({"type": "note", "text": note, "ts": time.time()})
            save_history(history)
            return "📝 Noted."
        return "What should I remember?"
    if low == "notes":
        if notes:
            return "\n".join(f"{i}. {n}" for i, n in enumerate(notes, 1))
        return "No notes yet."
    if low == "clear notes":
        history = [h for h in history if h.get("type") != "note"]
        save_history(history)
        return "🧹 Notes cleared."
    if low.startswith("weather "):
        city = text.split(" ", 1)[1].strip()
        return weather_for(city)
    if low == "weather":
        return "Try: weather Newark"
    return "I didn't get that. Type 'help' for options."

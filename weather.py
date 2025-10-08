# ============================================
# weather.py - Zone-based weather system for Flight AURORA
# ============================================

import random

# Weather options for each zone
ZONE_WEATHER = {
    "Reality": [
        {"condition": "Clear Skies", "fuel_penalty": 0, "crash_chance": 0.0},
        {"condition": "Light Clouds", "fuel_penalty": 2, "crash_chance": 0.0}
    ],
    "Transition": [
        {"condition": "Radio Static", "fuel_penalty": 3, "crash_chance": 0.0},
        {"condition": "Foggy Horizon", "fuel_penalty": 5, "crash_chance": 0.05}
    ],
    "Twilight": [
        {"condition": "Phantom Fog", "fuel_penalty": 6, "crash_chance": 0.1},
        {"condition": "Shifting Lights", "fuel_penalty": 8, "crash_chance": 0.15}
    ],
    "Crisis": [
        {"condition": "Thunderstorm", "fuel_penalty": 10, "crash_chance": 0.2},
        {"condition": "Lightning Storm", "fuel_penalty": 12, "crash_chance": 0.25}
    ],
    "Aurora": [
        {"condition": "Storm Wall", "fuel_penalty": 15, "crash_chance": 0.3},
        {"condition": "False Lights", "fuel_penalty": 18, "crash_chance": 0.35}
    ]
}


import random

def get_weather(zone_name):
    """Return weather conditions that depend on the zone."""

    conditions = [
        {"condition": "Clear Skies ☀️", "fuel_penalty": 0, "crash_chance": 0.02},
        {"condition": "Mild Winds 🌤", "fuel_penalty": 3, "crash_chance": 0.05},
        {"condition": "Rainstorm 🌧", "fuel_penalty": 5, "crash_chance": 0.15},
        {"condition": "Thunderstorm ⛈", "fuel_penalty": 10, "crash_chance": 0.35},
        {"condition": "Snowstorm ❄️", "fuel_penalty": 7, "crash_chance": 0.20},
        {"condition": "Cyclone 🌪", "fuel_penalty": 15, "crash_chance": 0.60},
    ]

    # Zone-based weighting
    if "Reality" in zone_name:
        weights = [0.5, 0.3, 0.2, 0, 0, 0]   # Mostly easy
    elif "Transition" in zone_name:
        weights = [0.3, 0.3, 0.25, 0.15, 0, 0]
    elif "Twilight" in zone_name:
        weights = [0.1, 0.2, 0.3, 0.25, 0.15, 0]
    elif "Crisis" in zone_name:
        weights = [0.05, 0.1, 0.25, 0.3, 0.2, 0.1]
    elif "Aurora" in zone_name:
        weights = [0, 0.05, 0.15, 0.3, 0.25, 0.25]  # Brutal endgame
    else:
        weights = [1/len(conditions)] * len(conditions)

    return random.choices(conditions, weights=weights, k=1)[0]




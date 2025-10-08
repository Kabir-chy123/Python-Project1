# ============================================
# world.py - Flight AURORA Game World
# ============================================

from database import fetch_airports, phantom_airports, aurora_airport
from clue_bank import CLUE_BANK
import random

# -------------------------------
# Helper: get clue for airport
# -------------------------------
def get_airport_clue(airport, zone_prefix=""):
    key = airport.get("id") or airport.get("ident")

    # Fallback clues if ID not in CLUE_BANK
    if key not in CLUE_BANK:
        if zone_prefix == "Reality":
            key = random.choice(["R001","R002","R003"])
        elif zone_prefix == "Transition":
            key = random.choice(["T001","T002","T003"])
        elif zone_prefix == "Twilight":
            key = "TSAFE"
        elif zone_prefix == "Crisis":
            key = random.choice(["C001","C002","C003"])
        elif zone_prefix == "Aurora":
            key = "F-FINAL"
    return CLUE_BANK.get(key, "No clue recorded.")

# -------------------------------
# Build Game World Zones
# -------------------------------
def build_game_world():
    return {
        "Reality Zone": {
            "description": "Safe skies with stable airports.",
            "airports": fetch_airports(limit=3, airport_type="large_airport"),
            "prefix": "Reality"
        },
        "Transition Zone": {
            "description": "Airports seem normal, but static creeps into the radios.",
            "airports": fetch_airports(limit=3, airport_type="medium_airport"),
            "prefix": "Transition"
        },
        "Twilight Zone": {
            "description": "Phantom and real airports mix. One wrong choice ends your journey.",
            "airports": phantom_airports + fetch_airports(limit=2, airport_type="medium_airport"),
            "prefix": "Twilight"
        },
        "Crisis Zone": {
            "description": "Storms rage, survivors call for help. Every choice costs fuel.",
            "airports": fetch_airports(limit=3, airport_type="all"),
            "prefix": "Crisis"
        },
        "Aurora Frontier": {
            "description": "The final storm corridor. Aurora Beacon or false lights?",
            "airports": [
                aurora_airport,
                {"id": "X-FALSE", "name": "False Lights Airfield", "effect": "trap", "zone": "Aurora"},
                {"id": "X-STORM", "name": "Storm Corridor", "effect": "death", "zone": "Aurora"}
            ],
            "prefix": "Aurora"
        }
    }




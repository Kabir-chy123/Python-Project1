from database import fetch_runs, save_run, save_progress, load_progress
import random
import sys
import mysql.connector
import math
import os
import time

from World import build_game_world, get_airport_clue
from dialogue import (
    intro_dialogue, nova_transition_warning, nova_twilight_warning,
    nova_crisis_warning, nova_final_warning, cartographer_dialogue,
    nova_dynamic_commentary, nova_dynamic_comment
)
from weather import get_weather
from hud import create_player, show_hud, update_fuel, rescue_survivors, lose_chance, change_zone, add_item, show_inventory, choose_role, choose_difficulty, show_map_progress
from endings import check_ending

# =====================================================================
# Distance & Fuel Calculation
# =====================================================================
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine formula to calculate distance (km) between two airports.
    """
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def calculate_fuel_cost(origin, destination, weather, player=None):
    """
    Fuel cost = base + distance/100 + weather penalty
    origin, destination are (ident, name, country, lat, lon)
    """
    lat1, lon1 = origin[3], origin[4]
    lat2, lon2 = destination[3], destination[4]
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    base_cost = 10
    fuel_cost = base_cost + (distance / 100) + weather["fuel_penalty"]

    # ▼ Engineer role → 20% less fuel
    if player and player.get("role") == "Engineer":
        fuel_cost = int(fuel_cost * 0.8)
        print("🔧 Engineer skill reduces fuel consumption!")

    # ▼ Engine Upgrade → extra 10% reduction (stacks with Engineer)
    if player and player.get("engine_boost", False):
        fuel_cost = int(fuel_cost * 0.9)
        print("⚙️ Engine upgrade efficiency bonus active!")

    return int(fuel_cost)
# =====================================================================
# Random Flight Events
# =====================================================================
def random_flight_event(player):
    """Trigger a random event during flight, with role effects."""
    event_roll = random.random()

    if event_roll < 0.20:
        print("🌬️ Tailwind! You save 5 fuel.")
        update_fuel(player, -5)  # give back fuel

    elif event_roll < 0.40:
        print("⚠️ Turbulence shakes the plane! You lose 5 fuel.")
        update_fuel(player, 5)
        # Navigator helps here
        if player.get("role") == "Navigator":
            update_fuel(player, -3)  # Navigator reduces penalty
            print("🧭 Navigator skill helps steady the flight (reduced loss).")

    elif event_roll < 0.60:
        print("🔧 Minor mechanical issue detected...")
        # Engineer helps here
        if player.get("role") == "Engineer":
            print("🔧 Engineer fixes it quickly — no fuel lost!")
        else:
            update_fuel(player, 5)
            print("⚠️ Without an Engineer, it costs 5 extra fuel.")

    elif event_roll < 0.80:
        print("📻 Survivor radio signal detected...")
        # Leader helps here
        if player.get("role") == "Leader":
            print("👥 Leader convinces them to join — you gain +1 survivor!")
            rescue_survivors(player, 1)
        else:
            print("The signal fades before you can respond.")

    else:
        print("☀️ Clear skies ahead. Smooth flight.")
# =====================================================================
# Fuel Upgrade & Refueling System
# =====================================================================
def refuel_or_upgrade(player):
    """Chance to refuel or find upgrade at airports."""
    chance = random.random()

    # 15% chance for refueling station
    if chance < 0.15:
        gained = random.randint(15, 40)
        player["fuel"] = min(150, player["fuel"] + gained)
        print(f"⛽ You found a refueling station! +{gained} fuel added.")

    # 10% chance to find upgrades
    elif chance < 0.25:
        upgrade = random.choice(["Extra Fuel Tank", "Engine Upgrade"])
        add_item(player, upgrade)
        print(f"🔩 You discovered a rare upgrade: {upgrade}!")

        # Apply benefits
        if upgrade == "Extra Fuel Tank":
            player["fuel"] = min(200, player["fuel"] + 50)
            print("💨 Max fuel temporarily increased to 200!")
        elif upgrade == "Engine Upgrade":
            player["engine_boost"] = True
            print("⚙️ Engine upgrade active — fuel cost reduced by 10%!")

    else:
        print("🛫 Nothing special found at this stop.")

def branching_story_event(player, zone_name):
    """Trigger a zone-based branching narrative event."""
    if "Transition" in zone_name:
        print("\n🌌 You detect a strange shimmering runway in the distance...")
        print(" 1. 🛬 Land and investigate")
        print(" 2. ✈️ Stay on course")
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            update_fuel(player, 10)
            if random.random() < 0.5:
                add_item(player, "Storm Compass")
                print("✨ You found a Storm Compass!")
            else:
                print("⚠️ The runway collapses, wasted fuel.")
        return None  # continue game

    elif "Twilight" in zone_name:
        print("\n👻 A ghostly radio whispers coordinates...")
        print(" 1. Follow it")
        print(" 2. Shut off the radio")
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            if random.random() < 0.3:
                lose_chance(player)
                print("👻 It was a phantom trap! You lose a chance.")
                if player["chances"] <= 0:
                    return check_ending(player, "GHOST")  # new ghost ending
            else:
                add_item(player, "Fuel Canister")
                print("🛢️ You found a Fuel Canister in an old hangar.")
        else:
            print("📻 You cut the radio and avoid distraction.")
        return None

    elif "Crisis" in zone_name:
        print("\n🚨 A military outpost requests help!")
        print(" 1. Divert to assist")
        print(" 2. Stay on mission")
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            update_fuel(player, 15)
            rescue_survivors(player, 2)
            print("👥 You rescued 2 survivors, but lost 15 fuel.")
            if player["survivors"] >= 10:
                return check_ending(player, "SURVIVOR")  # special ending
        else:
            lose_chance(player)
            print("⚠️ Survivors abandoned. You lose 1 chance.")
        return None

    elif "Aurora" in zone_name:
        print("\n🌠 A dazzling aurora storm blocks your path...")
        print(" 1. Push through")
        print(" 2. Wait it out")
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            if random.random() < 0.4:
                print("⚡ The storm destroys your plane!")
                return check_ending(player, "STORM")
            else:
                player["fuel"] = min(150, player["fuel"] + 50)
                print("✨ You brave the storm and gain mysterious energy! Fuel +50.")
        else:
            print("⏳ You wait until the storm passes safely.")
        return None

# =====================================================================
# NOVA Weather Prediction System
# =====================================================================
def nova_weather_prediction(next_zone):
    """Predicts the possible weather type in the next zone."""
    possible_weathers = {
        "Reality": "Stable skies ahead — minor cloud formations detected.",
        "Transition": "Sensors picking up interference — fog or radio static likely.",
        "Twilight": "Readings unstable — phantom anomalies or dense fog expected.",
        "Crisis": "Severe turbulence forming — thunder activity increasing.",
        "Aurora": "Massive storm front detected — unpredictable electromagnetic fields."
    }

    # Random variation for realism
    uncertainty = random.choice([
        "Confidence: 90%.",
        "Confidence: 75%.",
        "Confidence: 50%. Conditions may change suddenly."
    ])

    message = possible_weathers.get(next_zone, "Data unavailable for unknown region.")
    print(f"\n🔮 NOVA Forecast: {message} {uncertainty}")

# =====================================================================
# NOVA Weather Alert System
# =====================================================================
def nova_weather_alert(weather):
    """Give dynamic warnings based on weather danger level."""
    condition = weather["condition"]
    crash_risk = weather["crash_chance"]

    if crash_risk >= 0.5:
        print(f"\n🚨 NOVA: 'Pilot, this is madness! {condition} ahead — systems at maximum alert!'")
    elif crash_risk >= 0.3:
        print(f"\n⚠️ NOVA: 'Severe turbulence detected! Brace for impact — {condition} approaching.'")
    elif crash_risk >= 0.15:
        print(f"\n⚡ NOVA: 'Winds unstable. We’re flying through {condition}. Stay sharp, pilot.'")
    elif crash_risk >= 0.05:
        print(f"\n🌤 NOVA: 'Light disturbances in the atmosphere... {condition}, proceed carefully.'")
    else:
        print(f"\n☀️ NOVA: 'Skies are calm, pilot. {condition} ahead — clear flight path.'")

# =====================================================================
# NOVA Dynamic Dialogue System
# =====================================================================
def nova_dynamic_comment(player, context=""):
    """NOVA reacts dynamically to player’s state and context."""
    fuel = player.get("fuel", 0)
    survivors = player.get("survivors", 0)
    chances = player.get("chances", 0)

    if fuel < 20:
        print("💬 NOVA: 'Warning, Pilot — fuel reserves critical. I can almost hear the engines begging for mercy.'")
    elif survivors >= 5:
        print("💬 NOVA: 'You’ve turned this flight into an ark, Pilot. The skies owe you their gratitude.'")
    elif chances == 1:
        print("💬 NOVA: 'One last chance, one last storm. Let’s make it count.'")
    elif "Storm Compass" in player.get("inventory", []):
        print("💬 NOVA: 'That compass hums when storms near. Almost... alive.'")

    if context == "crash_avoided":
        print("💬 NOVA: 'That was close. I’d call it luck — you’d call it skill.'")
    elif context == "rescue":
        print("💬 NOVA: 'Their faces... they’ll remember your wings, Pilot.'")

def show_minimap(current_zone):
    """Display a simple text-based mini map showing player progress."""
    zones = ["Reality", "Transition", "Twilight", "Crisis", "Aurora"]
    print("\n🗺️ Mini-Map Progress:")
    for z in zones:
        if z == current_zone:
            print(f" ▶️ [{z}]  <-- You are here")
        else:
            print(f"    {z}")
    print("-" * 40)

def nova_dynamic_dialogue(player, zone_name):
    """NOVA reacts dynamically to player state."""
    fuel = player.get("fuel", 0)
    survivors = player.get("survivors", 0)
    chances = player.get("chances", 0)

    if fuel < 20:
        print("⚠️ NOVA: 'Fuel levels critical. One more detour could end us, pilot.'")
    elif fuel > 120:
        print("💨 NOVA: 'Engines efficient. We’re gliding smooth, Captain.'")

    if survivors >= 5:
        print("💬 NOVA: 'Cabin chatter increasing — they believe in you.'")
    elif survivors == 0:
        print("🕯 NOVA: 'The cabin is empty… yet your mission continues.'")

    if chances <= 1:
        print("🚨 NOVA: 'We are running out of chances. Choose carefully.'")

    if "Storm Compass" in player.get("inventory", []):
        print("🧭 NOVA: 'The Storm Compass hums… it senses something beyond this zone.'")

    if "Aurora" in zone_name and fuel < 50:
        print("🌠 NOVA: 'We’re nearly there, but the light grows unstable… hurry, pilot.'")




# =====================================================================
# Main Game Loop
# =====================================================================

# ✨ Typing effect for cinematic feel
def type_text(text, delay=0.03):
    """Print text with typing animation."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ✨ Fancy divider
def divider():
    print("=============================================")

# 🧭 Animated Main Menu (with Resume Option)
def main_menu():
    """Animated main menu for Flight AURORA."""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        divider()
        type_text("           ✈️  FLIGHT AURORA SYSTEM BOOTING...", 0.02)
        divider()
        time.sleep(0.5)

        print("""
1. 🛫 Start New Mission
2. 🔁 Resume Last Flight
3. 🏆 View Hall of Fame
4. 📘 Instructions
5. ❌ Exit
""")
        choice = input("Select an option (1–5): ").strip()

        # --- Start New Game ---
        if choice == "1":
            os.system("cls" if os.name == "nt" else "clear")
            type_text("🛰️  Initializing systems...", 0.03)
            time.sleep(1)
            return "start"

        # --- Resume Saved Game ---
        elif choice == "2":
            os.system("cls" if os.name == "nt" else "clear")
            divider()
            type_text("🔁 RESUMING SAVED MISSION...", 0.02)
            divider()
            player, zone = load_progress()
            if player and zone:
                type_text(f"🧭 Save found! Resuming from {zone} Zone...", 0.03)
                time.sleep(1)
                return ("resume", player, zone)
            else:
                type_text("⚠️ No saved flight data detected. Start a new mission first.", 0.02)
                input("\nPress ENTER to return to menu...")

        # --- View Hall of Fame ---
        elif choice == "3":
            os.system("cls" if os.name == "nt" else "clear")
            divider()
            type_text("🏆 HALL OF FAME – Past Pilots", 0.02)
            divider()
            try:
                past_runs = fetch_runs()
                if past_runs:
                    for run in past_runs:
                        type_text(f"{run['played_at']} | {run['player_name']} → {run['ending']} "
                                  f"| Survivors: {run['survivors']} | Fuel Left: {run['fuel']}", 0.01)
                else:
                    type_text("No recorded pilots found. You could be the first.", 0.02)
            except Exception as e:
                type_text(f"⚠️ Database link error: {e}", 0.02)
            input("\nPress ENTER to return to menu...")

        # --- Instructions ---
        elif choice == "4":
            os.system("cls" if os.name == "nt" else "clear")
            divider()
            type_text("📘 FLIGHT AURORA – PILOT BRIEFING", 0.02)
            divider()
            type_text("""
🧭 MISSION OBJECTIVE:
    Locate and reach the Aurora Beacon — humanity’s last light.

⚙️ CONTROLS:
    - Choose options by typing numbers (1, 2, etc.).
    - Each flight consumes fuel. Manage wisely.
    - Weather affects crash risk and fuel use.

🪫 ROLES:
    - Engineer: Saves fuel.
    - Navigator: Reduces storm crash chance.
    - Leader: Rescues more survivors.

🌩️ REMINDER:
    Not all airports are real. Some whisper. Some vanish.
""", 0.01)
            input("Press ENTER to return to main menu...")

        # --- Exit ---
        elif choice == "5":
            os.system("cls" if os.name == "nt" else "clear")
            type_text("👋 Shutting down FLIGHT AURORA system...", 0.02)
            time.sleep(1)
            type_text("Goodbye, Pilot. The skies will remember you.", 0.03)
            sys.exit()

        else:
            type_text("⚠️ Invalid input. Please enter 1–5.", 0.02)
            time.sleep(1)


def story_intro():
    """Cinematic intro for Flight AURORA – personalized story start."""
    os.system("cls" if os.name == "nt" else "clear")
    print("=============================================")
    print("         ✈️  Welcome to Flight Aurora ")
    print("=============================================\n")
    time.sleep(2)

    # Ask for player name early
    player_name = input("🧭 Enter your pilot name: ").strip().title()
    os.system("cls" if os.name == "nt" else "clear")

    # --- Cinematic Story Begins ---
    print("🌌 [NARRATOR] The world above the clouds has changed.")
    time.sleep(3)
    print("🌌 [NARRATOR] Airports flicker in and out of existence. Maps no longer hold meaning.")
    time.sleep(3)
    print("🌌 [NARRATOR] Some say a light still shines beyond the storm — the Aurora Beacon.")
    time.sleep(4)

    print("\n💫 SYSTEM BOOT: AI NAVIGATOR – NOVA ONLINE.")
    time.sleep(2)
    print(f"NOVA: 'Pilot {player_name}, systems are unstable... but you’re still here.'")
    time.sleep(3)
    print(f"NOVA: 'Our world is vanishing, one airport at a time. You’re the last pilot still transmitting.'")
    time.sleep(4)
    print(f"NOVA: 'Your mission, {player_name}: locate and reach the Aurora Beacon.'")
    time.sleep(3)
    print("NOVA: 'It’s the last signal left in the northern sky… and maybe humanity’s last hope.'")
    time.sleep(4)

    print("\n⚠️ SYSTEM CHECK:")
    print("   ✈️ Fuel System: ONLINE")
    print("   🧭 Navigation: UNSTABLE")
    print("   ☁️ Weather Forecast: CHAOTIC")
    print("   💾 Database Link: ACTIVE")
    time.sleep(3)

    print(f"\nNOVA: 'I’ll guide you, {player_name}, but your instincts will decide your fate.'")
    time.sleep(3)
    print("NOVA: 'Ready your engines... the sky won’t wait much longer.'")
    input("\n🔹 Press ENTER to begin your journey... ")
    os.system("cls" if os.name == "nt" else "clear")

    return player_name

def run_game(player_name, resume=False, start_zone=None):
    # === 🏆 Show Hall of Fame ===
    try:
        past_runs = fetch_runs()
        print("=== 🏆 HALL OF FAME ===")
        # 🧭 Load saved progress if resuming
        if resume:
            print(f"🔁 Resuming previous mission from {start_zone} Zone...\n")
            player, _ = load_progress()
        else:
            player = create_player()
        if past_runs:
            for run in past_runs:
                print(f"{run['played_at']} | {run['player_name']} → {run['ending']} "
                      f"| Survivors: {run['survivors']} | Fuel Left: {run['fuel']}")
        else:
            print("No past pilots recorded yet.")
        print("========================\n")
    except Exception as e:
        print("⚠️ Could not load Hall of Fame:", e)

    # Build world zones
    game_world = build_game_world()

    # === Choose difficulty ===
    difficulty = choose_difficulty()
    player["difficulty"] = difficulty

    if difficulty == "Easy":
        player["fuel"] = 150
        player["chances"] = 5
    elif difficulty == "Normal":
        player["fuel"] = 100
        player["chances"] = 3
    elif difficulty == "Hard":
        player["fuel"] = 70
        player["chances"] = 2

    print(f"\n🎮 Difficulty set to {difficulty}! Starting with {player['fuel']} fuel and {player['chances']} chances.")
    player["role"] = choose_role()
    print(f"\n✨ You are playing as a {player['role']}!\n")

    # Progress through zones in order
    for zone_name, data in game_world.items():
        # --- Resume logic: skip earlier zones ---
        if resume and start_zone:
            if zone_name != start_zone:
                continue  # skip zones before the saved one
            else:
                resume = False  # once we hit saved zone, start from here
        change_zone(player, zone_name.replace(" Zone", ""))

        print("\n=====================================")
        print(f"🌍 Entering {zone_name}")
        show_map_progress(zone_name)
        show_minimap(zone_name)
        print(data["description"])
        # NOVA gives a short comment on the new zone
        nova_dynamic_dialogue(player, zone_name)
        show_hud(player)
        show_inventory(player)
        # Apply weather after mid-flight events
        weather = get_weather(zone_name)
        print(
            f"☁️ Weather: {weather['condition']} | Fuel Penalty: {weather['fuel_penalty']} | Crash Chance: {weather['crash_chance'] * 100:.0f}%")
        nova_weather_alert(weather)
        nova_dynamic_comment(player, "weather")

        refuel_or_upgrade(player)

        # (flight logic here...)
        # NOVA checks in before next jump
        nova_dynamic_comment(player, "end_zone")

        # Show HUD
        show_hud(player)
        show_inventory(player)

        # Zone-specific warnings
        if "Transition" in zone_name:
            nova_transition_warning()
        elif "Twilight" in zone_name:
            nova_twilight_warning()
            cartographer_dialogue()
        elif "Crisis" in zone_name:
            nova_crisis_warning()
        elif "Aurora" in zone_name:
            nova_final_warning()

        # NOVA gives a weather prediction for the next zone
        nova_weather_prediction(zone_name)

        # Show airports
        print("\nAirports in this zone:")
        for idx, airport in enumerate(data["airports"], start=1):
            if "effect" in airport:  # phantom/aurora airports
                print(f" {idx}. {airport['id']} | {airport['name']} (Effect: {airport['effect']})")
            else:  # real DB airports
                print(f" {idx}. {airport['ident']} | {airport['name']} ({airport['iso_country']}) [{airport['type']}]")
            print(f"    ✧ Clue: {get_airport_clue(airport, data['prefix'])}")

        # Player chooses
        try:
            choice = int(input("Choose your destination (number): ")) - 1
            chosen_airport = data["airports"][choice]
        except (ValueError, IndexError):
            print("⚠️ Invalid input! Defaulting to first airport.")
            chosen_airport = data["airports"][0]

        # Random mid-flight event
        random_flight_event(player)

        # Apply weather
        weather = get_weather(zone_name)
        print(
            f"☁️ Weather: {weather['condition']} | Fuel Penalty: {weather['fuel_penalty']} | Crash Chance: {weather['crash_chance'] * 100:.0f}%")
        nova_weather_alert(weather)
        # NOVA reacts dynamically to weather and current status
        nova_dynamic_comment(player, "weather")

        # Fuel cost (distance + weather)
        if "ident" in chosen_airport:
            origin = (chosen_airport['ident'], chosen_airport['name'], chosen_airport['iso_country'],
                      random.uniform(-60, 60), random.uniform(-120, 120))
            dest = (chosen_airport['ident'], chosen_airport['name'], chosen_airport['iso_country'],
                    random.uniform(-60, 60), random.uniform(-120, 120))
            fuel_cost = calculate_fuel_cost(origin, dest, weather, player)
        else:
            # phantom airports (no coords, so flat cost)
            fuel_cost = 15 + weather["fuel_penalty"]
            if player.get("role") == "Engineer":
                fuel_cost = int(fuel_cost * 0.8)
                print("🔧 Engineer skill reduces fuel consumption!")

        update_fuel(player, fuel_cost)
        print(f"🛢️ Fuel consumed: {fuel_cost} | Remaining: {player['fuel']}")

        refuel_or_upgrade(player)
        nova_dynamic_commentary(player)

        # 25% chance to trigger a branching story event
        if random.random() < 0.25:
            outcome = branching_story_event(player, zone_name)
            if outcome:  # if event ends game (Aurora storm crash)
                return outcome, player_name, player


        # === Special branching endings in Aurora zone ===
        if "Aurora" in zone_name:
            # Compass Ending (if Storm Compass is in inventory)
            if "Storm Compass" in player["inventory"]:
                return check_ending(player, "COMPASS"), player_name, player

            # Rebellion Ending (player choice)
            rebellion_choice = input("\n🚀 You see Aurora Beacon shining ahead... Do you want to turn away and forge your own path? (y/n): ").lower()
            if rebellion_choice == "y":
                return check_ending(player, "REBELLION"), player_name, player

        # Apply inventory effects on crash chance
        crash_chance = weather["crash_chance"]

        if "Storm Shield" in player["inventory"]:
            crash_chance *= 0.5
            print("🛡️ Storm Shield reduces crash chance!")

        # Role effect: Navigator
        if player.get("role") == "Navigator":
            crash_chance *= 0.8
            print("🧭 Navigator skill reduces phantom crash risk!")

        # Crash roll
        if random.random() < crash_chance:
            print("⚡ The storm overwhelms you!")
            result = check_ending(player, "STORM"), player_name, player
            return result, player_name, player

        # Phantom airports effects
        if "effect" in chosen_airport:
            effect = chosen_airport["effect"]
            if effect == "win":
                result = check_ending(player, "AURORA"),
                return result, player_name, player
            elif effect == "trap":
                result = check_ending(player, "LOOP"),
                return result, player_name, player
            elif effect == "stranded":
                result = check_ending(player, "DEC"),
                return result, player_name, player
            elif effect == "crash":
                result = check_ending(player, "HAUNT"),
                return result, player_name, player
            elif effect == "death":
                result = check_ending(player, "STORM"),
                return result, player_name, player

        # Crisis zone → survivor mission
        if "Crisis" in zone_name and random.random() < 0.5:  # 50% chance
            print("\n🚨 Distress call detected! Survivors need rescue.")
            action = input("Do you want to rescue them? (y/n): ").lower()
            if action == "y":
                print("🛬 You land and rescue survivors, but it costs extra fuel.")
                rescue_survivors(player, 1)
                update_fuel(player, 5)
                nova_dynamic_comment(player, "end_zone")
                # Chance to find item
                chance = 0.3
                if player.get("role") == "Leader":
                    chance = 0.45  # Leaders inspire survivors more
                if random.random() < chance:
                    add_item(player, "Storm Shield")
                    print("✨ You found a Storm Shield! Crash risk reduced.")
            else:
                print("🛫 You ignore the call. Fuel saved, but survivors left behind.")
                from database import save_progress
                save_progress(player, zone_name)
    # If reached here, final ending check
    # 💾 Auto-save progress at end of each zone
    save_progress(player, zone_name)
    print(f"💾 Progress saved! You can resume from {zone_name} next time.")
    result = check_ending(player, "AURORA")
    return result, player_name, player

# =====================================================================
# Run
# =====================================================================
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    # 🧭 Show Main Menu (Start / Resume / Hall of Fame / Instructions / Exit)
    menu_action = main_menu()

    # ✈️ Start a New Mission
    if menu_action == "start":
        player_name = story_intro()
        os.system("cls" if os.name == "nt" else "clear")
        result, _, player = run_game(player_name)

    # 🔁 Resume a Saved Mission
    elif isinstance(menu_action, tuple) and menu_action[0] == "resume":
        _, player, zone = menu_action
        os.system("cls" if os.name == "nt" else "clear")
        print(f"🧭 Resuming mission from {zone} Zone...")
        result, _, player = run_game(player["player_name"], resume=True, start_zone=zone)
    # 🏁 Show Final Results
    print(f"\n=== GAME OVER: {result} ===")
    try:
        save_run(player["player_name"], result, player["survivors"], player["fuel"])
        print("🏆 Your run has been saved to the Hall of Fame!")
    except Exception as e:
        print("⚠️ Could not save run:", e)






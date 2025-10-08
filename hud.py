# ============================================
# hud.py – Player HUD & Core Gameplay Utilities
# ============================================
import sys
import time
import random

# ============================================================
# PLAYER CREATION
# ============================================================
def create_player():
    """Initialize a new player profile."""
    return {
        "fuel": 100,
        "survivors": 0,
        "chances": 3,
        "zone": "Reality",
        "inventory": [],
        "role": None,
        "difficulty": "Normal",
        "engine_boost": False
    }


# ============================================================
# HUD DISPLAY
# ============================================================
def show_hud(player):
    """Display player stats neatly in HUD format."""
    print("\n=====================================")
    print("🧭  FLIGHT STATUS – AURORA HUD")
    print("=====================================")
    print(f"✈️  Zone: {player.get('zone', 'Unknown')}")
    print(f"⛽ Fuel: {player.get('fuel', 0)}")
    print(f"👥 Survivors: {player.get('survivors', 0)}")
    print(f"❤️ Chances: {player.get('chances', 0)}")
    print(f"🎮 Role: {player.get('role', 'Unassigned')}")
    print("=====================================\n")


# ============================================================
# FUEL MANAGEMENT
# ============================================================
def update_fuel(player, amount):
    """Increase or decrease fuel, clamped safely between 0 and 200."""
    player["fuel"] = max(0, min(200, player.get("fuel", 0) - amount))
    if player["fuel"] <= 0:
        print("⚠️  WARNING: Fuel depleted! Systems critical.")


# ============================================================
# SURVIVOR & CHANCE MANAGEMENT
# ============================================================
def rescue_survivors(player, count=1):
    """Add rescued survivors to player data."""
    player["survivors"] += count
    print(f"👥 {count} survivor(s) rescued! Total: {player['survivors']}")

def lose_chance(player):
    """Reduce a player chance after failure."""
    player["chances"] = max(0, player["chances"] - 1)
    print(f"💔 You lost a chance. Remaining chances: {player['chances']}")


# ============================================================
# INVENTORY MANAGEMENT
# ============================================================
def add_item(player, item):
    """Add an item to the player's inventory."""
    if "inventory" not in player:
        player["inventory"] = []
    if item not in player["inventory"]:
        player["inventory"].append(item)
        print(f"🎒 Added to inventory: {item}")
    else:
        print(f"🧳 You already have {item}.")


def show_inventory(player):
    """Display the player’s current inventory."""
    print("\n🎒 INVENTORY:")
    if not player["inventory"]:
        print("   (Empty)")
    else:
        for item in player["inventory"]:
            print(f"   - {item}")
    print("")


# ============================================================
# ZONE TRANSITIONS
# ============================================================
def change_zone(player, new_zone):
    """Change the player’s current zone."""
    player["zone"] = new_zone
    print(f"🌍 Transitioning into {new_zone} Zone...")


# ============================================================
# ROLE & DIFFICULTY SELECTION
# ============================================================
def choose_role():
    """Allow player to choose a special role."""
    roles = {
        "1": "Navigator 🧭 (Reduced crash chance)",
        "2": "Engineer 🔧 (Lower fuel cost)",
        "3": "Leader 👥 (Higher survivor rescue odds)"
    }
    print("\n🎭 Choose your role:")
    for key, desc in roles.items():
        print(f" {key}. {desc}")

    while True:
        choice = input("Enter role number: ").strip()
        if choice in roles:
            role_name = roles[choice].split()[0]
            print(f"✅ Role assigned: {roles[choice]}")
            return role_name
        print("❌ Invalid choice. Please select 1, 2, or 3.")


def choose_difficulty():
    """Allow player to select game difficulty."""
    print("\n🎯 Select Difficulty:")
    print(" 1.🟢  Easy   – More fuel & chances")
    print(" 2.🟡 Normal – Balanced experience")
    print(" 3.🔴Hard   – Real pilot challenge")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            print("🟢 Easy mode engaged.")
            return "Easy"
        elif choice == "2":
            print("🟡 Normal mode selected.")
            return "Normal"
        elif choice == "3":
            print("🔴 Hard mode — may the skies favor you.")
            return "Hard"
        print("❌ Invalid input. Try again.")


# ============================================================
# MAP PROGRESS (ASCII VISUALIZATION)
# ============================================================

def show_map_progress(zone_name):
    """Display visual progress through the 5 game zones with animation."""
    zones = ["Reality", "Transition", "Twilight", "Crisis", "Aurora"]
    progress = ["⬛"] * len(zones)

    if zone_name in zones:
        progress[zones.index(zone_name)] = "🟩"

    # --- Animated effect ---
    sys.stdout.write("\n🗺️ Updating flight path")
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.3)

    print("\n🗺️ Flight Path:", " → ".join(progress))
    print(f"   ✈️  Now entering: {zone_name} Zone\n")











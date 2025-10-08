# ============================================
# endings.py – Final outcomes for Flight AURORA
# ============================================

from dialogue import (
    ending_victory, ending_loop, ending_drowned,
    ending_haunt, ending_storm, ending_green_route,
    ending_mercenary, ending_hero, ending_ghost
)

# ============================================================
# Helper: Generate Final Summary
# ============================================================
def generate_summary(player):
    """Create a short dynamic summary for end credits."""
    fuel = player.get("fuel", 0)
    survivors = player.get("survivors", 0)
    role = player.get("role", "Pilot")
    items = player.get("inventory", [])
    summary = []

    summary.append(f"🧭 Final Role: {role}")
    summary.append(f"💨 Fuel Remaining: {fuel}")
    summary.append(f"👥 Survivors Rescued: {survivors}")

    if "Engine Upgrade" in items:
        summary.append("⚙️ Engine Upgrade Installed")
    if "Storm Compass" in items:
        summary.append("🧭 Storm Compass Found")
    if "Storm Shield" in items:
        summary.append("🛡️ Storm Shield Acquired")
    if "Extra Fuel Tank" in items:
        summary.append("⛽ Extended Fuel Capacity")

    return "\n".join(summary)


# ============================================================
# Main Function: Determine Ending
# ============================================================
def check_ending(player, final_choice):
    """
    Decide which ending to trigger based on player state and final choice.
    final_choice = 'AURORA', 'LOOP', 'DEC', 'HAUNT', 'STORM', etc.
    """

    # ============================================================
    # CRITICAL FAILURES
    # ============================================================
    if player["fuel"] <= 0:
        print("\n⚠️ Fuel tanks empty. Engines sputter in silence...")
        print("The cockpit goes dark as the storm swallows the plane whole.")
        ending_storm()
        return "Storm Failure"

    # ============================================================
    # SECRET & CONDITIONAL ENDINGS
    # ============================================================
    if player["survivors"] >= 3 and final_choice == "AURORA":
        print("\n🌱 Because you saved lives and flew wisely...")
        print("The world itself seems to respond. Clouds part, and a green-gold light emerges.")
        ending_green_route()
        return "Green Route"

    if final_choice == "LOOP":
        print("\n🔄 You circle back… again and again.")
        print("Each landing looks the same. Each takeoff drains more fuel.")
        print("At last, NOVA’s voice fades: 'Pilot… we are trapped.'")
        ending_loop()
        return "Loop Failure"

    if final_choice == "DEC":
        print("\n🌊 The runway seems real, but waves crash across it.")
        print("The wheels touch water. Engines choke. Alarms scream in vain.")
        print("Cold sea water fills the cabin as the plane disappears beneath the tide.")
        ending_drowned()
        return "Drowned Failure"

    if final_choice == "HAUNT":
        print("\n💀 The runway glows faintly, but shadows cling to it.")
        print("As you descend, fog thickens into hands pulling at the wings.")
        print("The ground gives way—there was never a runway here.")
        print("Your last sight is Aurora fading into mist.")
        ending_haunt()
        return "Haunted Failure"

    if final_choice == "STORM":
        print("\n⚡ Lightning blinds. Turbulence tears the plane apart.")
        print("Winds scream louder than NOVA’s failing systems.")
        print("One last bolt strikes—everything fades to black.")
        ending_storm()
        return "Storm Failure"

    # ============================================================
    # NEW EXPANDED ENDINGS
    # ============================================================
    if final_choice == "REBELLION":
        print("\n🚀 The plane tilts upward — beyond the storm, beyond the Beacon.")
        print("🛰️ NOVA: 'Pilot...? Where are you going?'")
        print("💫 Your signal disappears into the stars.")
        return "Rebellion Ending"

    if final_choice == "COMPASS":
        print("\n🧭 The Storm Compass glows, guiding you through impossible winds.")
        print("The storm bends as if obeying your will.")
        print("Aurora fades… but you soar into unknown skies.")
        return "Compass Ending"

    # ============================================================
    # MORAL OUTCOMES
    # ============================================================
    if final_choice == "AURORA" and player["survivors"] == 0:
        ending_mercenary()
        return "Mercenary Ending"

    if final_choice == "AURORA" and player["survivors"] >= 5:
        ending_hero()
        return "Hero Ending"

    if player["chances"] <= 0:
        ending_ghost()
        return "Ghost Ending"

    # ============================================================
    # TRUE VICTORY
    # ============================================================
    if final_choice == "AURORA":
        print("\n✨ Against all odds, you pass through the final storm.")
        print("The clouds open… and Aurora Beacon shines like a star reborn.")
        print("NOVA: 'Pilot… you made it.'")
        print("On the horizon, survivors gather at the light. The Cartographer is waiting.")
        ending_victory()
        return "Victory"

    # ============================================================
    # FINAL FALLBACK (AI-style outro)
    # ============================================================
    # Generate an AI-style closing line based on performance
    fuel = player.get("fuel", 0)
    survivors = player.get("survivors", 0)

    if fuel > 100:
        message = "‘You reached Aurora with power to spare. The skies still remember your courage.’"
    elif survivors >= 5:
        message = "‘You didn’t just fly — you saved humanity’s hope.’"
    elif fuel < 20:
        message = "‘Barely holding on... yet even the dimmest flame reaches the Beacon.’"
    else:
        message = "‘Through storm and silence, you proved humanity can still fly.’"

    fuel = player.get("fuel", 0)
    survivors = player.get("survivors", 0)
    print(f"\nNOVA (final transmission): {message}")
    print("🌠 Aurora fades — but your story becomes part of the light.")

    return "Unknown"


# ============================================================
# Cinematic Summary Screen
# ============================================================
def show_final_summary(player, result):
    """Display a cinematic wrap-up after the ending."""
    print("\n========================================")
    print("           ✨ FLIGHT AURORA ✨")
    print("========================================")
    print(f"🏁 Mission Result: {result}")
    print("\n" + generate_summary(player))
    print("========================================")
    print("NOVA: 'End of transmission… until next flight.'")
    print("========================================\n")









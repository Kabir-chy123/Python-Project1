# ============================================
# dialogue.py – Dynamic NOVA Dialogue System
# ============================================

import time
import random


def slow_print(text, delay=0.03):
    """Print text with a cinematic typing effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# ============================================
# Intro Dialogue
# ============================================
def intro_dialogue(player_name):
    slow_print(f"\n🛰️ NOVA: Initializing pilot systems... Welcome, {player_name}.")
    time.sleep(1)
    slow_print("🛰️ NOVA: The skies are collapsing. Airports flicker in and out of existence.")
    slow_print("🛰️ NOVA: Our mission is to reach the Aurora Beacon — the only stable point left.")
    slow_print("🛰️ NOVA: Fuel, survivors, choices... all of it will shape what remains of this world.")
    time.sleep(1)
    slow_print("🛰️ NOVA: Stay focused, Pilot. The skies are listening.")
    print("=============================================")
    time.sleep(1.2)


# ============================================
# Zone Warnings
# ============================================
def nova_transition_warning():
    slow_print("\n🛰️ NOVA: The skies ahead are unstable. Reality flickers at the edges.")
    slow_print("🛰️ NOVA: Not all runways will be where they appear.")
    time.sleep(1.2)

def nova_twilight_warning():
    slow_print("\n🌒 NOVA: Entering the Twilight Zone.")
    slow_print("🛰️ NOVA: Phantom signals, ghost airports — stay sharp, Pilot.")
    time.sleep(1.2)

def nova_crisis_warning():
    slow_print("\n⚠️ NOVA: Multiple distress calls incoming.")
    slow_print("🛰️ NOVA: This region is chaos — storms, survivors, and illusions overlap.")
    time.sleep(1.2)

def nova_final_warning():
    slow_print("\n🌠 NOVA: The Aurora Frontier.")
    slow_print("🛰️ NOVA: Readings are off the charts. Electromagnetic interference critical.")
    slow_print("🛰️ NOVA: The Beacon is near... but so is the storm that guards it.")
    time.sleep(1.5)


# ============================================
# The Cartographer
# ============================================
def cartographer_dialogue():
    slow_print("\n🧭 The Cartographer: 'You still chase the Beacon?'")
    slow_print("🧭 The Cartographer: 'Every pilot before you thought they were the first.'")
    slow_print("🧭 The Cartographer: 'Some lights are lures. Some storms are alive.'")
    slow_print("🧭 The Cartographer: 'Trust your instincts, not your instruments.'")
    time.sleep(1.5)


# ============================================
# Dynamic NOVA Commentary
# ============================================
def nova_dynamic_commentary(player):
    """NOVA dynamically reacts to player’s state."""
    fuel = player.get("fuel", 0)
    survivors = player.get("survivors", 0)
    chances = player.get("chances", 0)
    role = player.get("role", "Pilot")

    if fuel < 20:
        slow_print("\n🛰️ NOVA: Warning — fuel reserves at critical levels. I recommend immediate refueling.")
    elif fuel < 50:
        slow_print("\n🛰️ NOVA: Fuel levels below 50%. Every kilometer counts now.")
    elif fuel > 120:
        slow_print("\n🛰️ NOVA: Excellent fuel management, Pilot. Your efficiency is commendable.")

    if survivors >= 5:
        slow_print("🛰️ NOVA: You’ve saved many lives. Each one strengthens the signal toward Aurora.")
    elif survivors == 0:
        slow_print("🛰️ NOVA: No survivors aboard. The silence feels heavier than the storm.")

    if chances == 1:
        slow_print("🛰️ NOVA: Only one chance left, Pilot. Make it count.")
    elif chances == 0:
        slow_print("🛰️ NOVA: Systems detect zero operational chances... this may be the end.")

    if role == "Engineer":
        slow_print("🛰️ NOVA: Engineering analysis steady — your maintenance keeps us airborne.")
    elif role == "Leader":
        slow_print("🛰️ NOVA: The crew looks to you. Every decision carries weight.")
    elif role == "Navigator":
        slow_print("🛰️ NOVA: Navigational precision holding. The storm bends around your course.")


# ============================================
# Dynamic Reactions to Game Contexts
# ============================================
def nova_dynamic_comment(player, context="general"):
    """NOVA makes contextual comments based on in-game situations."""
    fuel = player.get("fuel", 0)
    survivors = player.get("survivors", 0)

    responses = {
        "weather": [
            "🛰️ NOVA: Atmospheric readings unstable — visibility may drop any moment.",
            "🛰️ NOVA: I'm detecting turbulence ahead. Adjusting thruster calibration.",
            "🛰️ NOVA: Temperature variance rising. Something unnatural is forming in these clouds."
        ],
        "end_zone": [
            "🛰️ NOVA: Zone transition complete. Calibrating new coordinates.",
            "🛰️ NOVA: Radiation interference decreasing — temporarily stable flight.",
            "🛰️ NOVA: Signal echoes fading. This region may be safe... for now."
        ],
        "danger": [
            "🛰️ NOVA: Warning! Electromagnetic surge detected!",
            "🛰️ NOVA: Brace for impact — anomaly approaching fast!",
            "🛰️ NOVA: Storm cell is expanding! Adjust altitude immediately!"
        ],
        "general": [
            "🛰️ NOVA: Monitoring systems... all stable for now.",
            "🛰️ NOVA: Your decisions alter the flight path more than you know.",
            "🛰️ NOVA: Somewhere in this chaos, there’s still hope."
        ]
    }

    line = random.choice(responses.get(context, responses["general"]))
    slow_print(f"\n{line}")


# ============================================
# Endings
# ============================================
def ending_victory():
    slow_print("\n🌅 NOVA: 'Pilot... you did it.'")
    slow_print("🛰️ The Beacon stabilizes the skies. One by one, the lost airports shimmer back into existence.")
    slow_print("🧭 The Cartographer watches in silence. 'You’ve rewritten the map, Pilot.'")
    slow_print("💫 The world breathes again.")
    time.sleep(2)

def ending_storm():
    slow_print("\n⚡ NOVA: 'System critical... Engines failing!'")
    slow_print("🌩️ Lightning consumes the cockpit. Every gauge spins red.")
    slow_print("🛰️ NOVA: 'We tried... Pilot... we...'")
    slow_print("💀 The storm wins.")
    time.sleep(2)

def ending_loop():
    slow_print("\n🔄 NOVA: 'Wait... Didn’t we land here before?'")
    slow_print("🌫️ The same runway. The same signal. Again and again.")
    slow_print("🛰️ NOVA: 'We’re trapped... in a loop that never ends.'")
    time.sleep(2)

def ending_drowned():
    slow_print("\n🌊 The plane descends into a mirage of blue.")
    slow_print("💀 The water closes over the wings. The ocean remembers you now.")
    slow_print("🛰️ NOVA: 'No response. Pilot signal lost.'")
    time.sleep(2)

def ending_haunt():
    slow_print("\n💀 The runway below flickers like a heartbeat.")
    slow_print("🌫️ Shadows climb the fuselage — reaching for the light in your eyes.")
    slow_print("🛰️ NOVA: '...Pilot?'")
    slow_print("👻 Silence answers.")
    time.sleep(2)

def ending_green_route():
    slow_print("\n🌱 Light turns emerald as the skies clear.")
    slow_print("🌤️ The Beacon pulses gently — not burning, but healing.")
    slow_print("🛰️ NOVA: 'You’ve given them hope... a new dawn for the skies.'")
    time.sleep(2)

def ending_mercenary():
    slow_print("\n💰 The Beacon rises behind you as you turn away.")
    slow_print("🛰️ NOVA: 'You had the chance to save them... and you chose yourself.'")
    slow_print("🌑 The world fades without its savior.")
    time.sleep(2)

def ending_hero():
    slow_print("\n🦸 NOVA: 'You saved them all. The skies sing your name, Pilot.'")
    slow_print("🌅 Survivors gather beneath the Beacon’s light — alive because of you.")
    slow_print("💫 The world will remember your flight.")
    time.sleep(2)

def ending_ghost():
    slow_print("\n👻 NOVA: 'No... this can’t be.'")
    slow_print("🌫️ The cockpit is empty, but the plane still flies.")
    slow_print("🛰️ NOVA: 'Pilot...? Who’s flying the ship?'")
    slow_print("💀 You’ve become part of the storm.")
    time.sleep(2)

def ending_compass():
    slow_print("\n🧭 The Storm Compass glows bright — its light bends the clouds aside.")
    slow_print("🛰️ NOVA: 'Impossible... The storm obeys you.'")
    slow_print("💫 You fly beyond the world’s edge, guided by the compass of destiny.")
    time.sleep(2)

def ending_rebellion():
    slow_print("\n🚀 You cut communication with NOVA.")
    slow_print("🌌 The plane tilts upward — beyond the storm, beyond the Beacon.")
    slow_print("🛰️ NOVA: 'Pilot...? Where are you going?'")
    slow_print("💫 Your signal disappears into the stars.")
    time.sleep(2)



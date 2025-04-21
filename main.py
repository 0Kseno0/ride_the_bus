import pyautogui
import time
import random
from card_reader import take_card_screenshot, recognize_card

# Coordinates of Buttons/Clicks
# Read card Area: 880 400 - 1040 610

# Ready button: 950 700

# Stage 1 & 2 & 3 buttons:
#   Red: 950 750
#   Black: 950 800
#   Forfeit: 950 850

# Stage 4 buttons:
#   Hearts: 950 750
#   Clubs: 950 800
#   Diamond: 950 850
#   Spades: 950 900
#   Forfeit: 950 950

CARD_REGION = (880, 400, 160, 210)

# button coordinates:
POSITIONS = {
    "start_game": (950, 700),
    "red": (950, 750),
    "higher": (950, 750),
    "lower": (950, 800),
    "cashout_phase2": (950, 850),
    "inside": (950, 750),
    "outside": (950, 800),
    "cashout_phase3": (950, 850),
    "hearts": (950, 750),
    "clubs": (950, 800),
    "diamonds": (950, 850),
    "spades": (950, 900),
}

# Mapping of card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'jack': 11, 'queen': 12, 'king': 13, 'ace': 14
}

def click(position_name):
    x, y = POSITIONS[position_name]
    pyautogui.click(x, y)
    print(f"Clicked on {position_name}")

def read_card():
    img_path = take_card_screenshot(CARD_REGION)
    value, suit = recognize_card(img_path)
    if value and suit:
        print(f"Card detected: {value} of {suit}")
        return value, suit
    else:
        print("No card detected!")
        return None, None

def decide_phase2(first_card_value):
    """decision of phase 2: higher, lower or forfeit"""
    num = CARD_VALUES.get(first_card_value, 0)
    if num < 9:
        click("higher")
        return "higher"
    elif num > 9:
        click("lower")
        return "lower"
    else:
        click("cashout_phase2")
        return "cashout"

def decide_phase3(first_value, second_value):
    """decision for phase 3: inside, outside or forfeit"""
    num1 = CARD_VALUES.get(first_value, 0)
    num2 = CARD_VALUES.get(second_value, 0)
    diff = abs(num1 - num2)
    if diff > 7:
        click("inside")
        return "inside"
    elif diff < 5:
        click("outside")
        return "outside"
    else:
        click("cashout_phase3")
        return "cashout"

def decide_symbol(known_suits):
    """decision for phase 4: card symbol"""
    all_suits = ['hearts', 'clubs', 'diamonds', 'spades']
    suit_counts = {suit: 0 for suit in all_suits}

    for suit in known_suits:
        suit_counts[suit] += 1

    max_missing = max((3 - suit_counts[suit]) for suit in all_suits)
    best_choices = [suit for suit in all_suits if (3 - suit_counts[suit]) == max_missing]

    choice = random.choice(best_choices)
    click(choice)
    print(f"Symbol chosen: {choice}")
    return choice

def check_phase1_answer(first_card_suit, decision):
    if decision == "red":
        return first_card_suit in ["hearts", "diamonds"]
    elif decision == "black":
        return first_card_suit in ["spades", "clubs"]
    return False

def check_phase2_answer(first_card_value, second_card_value, decision):
    num1 = CARD_VALUES.get(first_card_value, 0)
    num2 = CARD_VALUES.get(second_card_value, 0)

    if decision == "higher":
        return num2 >= num1
    elif decision == "lower":
        return num2 < num1
    elif decision == "cashout":
        return True
    return False

def check_phase3_answer(first_card_value, second_card_value, third_card_value, decision):
    num1 = CARD_VALUES.get(first_card_value, 0)
    num2 = CARD_VALUES.get(second_card_value, 0)
    num3 = CARD_VALUES.get(third_card_value, 0)

    low = min(num1, num2)
    high = max(num1, num2)

    if decision == "inside":
        return low-1 < num3 < high+1
    elif decision == "outside":
        return num3 < low or num3 > high
    elif decision == "cashout":
        return True
    return False

def main():
    while True:
        print("Starting new playthrough...")

        time.sleep(2)

        # --- Phase 0: Start Ride the Bus ---
        click("start_game")
        time.sleep(2)

        # --- Phase 1: decision irrelevant, black may be chosen aswell ---
        click("red")
        time.sleep(2)

        # --- read card 1 ---
        first_value, first_suit = read_card()
        if not first_value:
            continue  # restart if no card is detected

        # --- check if phase 1 answer was correct ---
        if not check_phase1_answer(first_suit, "red"):  # if red was exchanged for black previously, insert black for red aswell
            print("Phase 1 decision wrong! Restarting.")
            continue

        time.sleep(3)

        # --- Phase 2: higher/lower/forfeit ---
        decision2 = decide_phase2(first_value)
        time.sleep(2)

        # --- read card 2 ---
        second_value, second_suit = read_card()
        if not second_value:
            continue  # restart

        # --- check phase 2 ---
        if not check_phase2_answer(first_value, second_value, decision2):
            print("Phase 2 decision wrong! Restarting.")
            continue

        time.sleep(3)

        # --- Phase 3: inside/outside/forfeit ---
        decision3 = decide_phase3(first_value, second_value)
        time.sleep(2)

        # --- read card 3 ---
        third_value, third_suit = read_card()
        if not third_value:
            continue

        # --- check phase 3 ---
        if not check_phase3_answer(first_value, second_value, third_value, decision3):
            print("Phase 3 decision wrong! Restarting.")
            continue

        time.sleep(3)

        # --- Phase 4: choose symbol ---
        known_suits = [first_suit, second_suit, third_suit]
        decide_symbol(known_suits)

        # --- wait for new playthrough ---
        time.sleep(4)

if __name__ == "__main__":
    main()

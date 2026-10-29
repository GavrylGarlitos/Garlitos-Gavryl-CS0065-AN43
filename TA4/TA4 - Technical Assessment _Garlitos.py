# PART 1: KNOWLEDGE REPRESENTATION (KR)
# Task 1A - Create a Knowledge Base


facts = {
    "power_connected": True,
    "battery_charged": False,
    "power_light": False,
    "screen_visible": False,
    "fan_noise": False,
    "overheating": False,
    "wifi_connected": True,
    "temperature": 45
}

# Three categories of knowledge
categories = {
    "power_status": ["power_connected", "battery_charged", "power_light"],
    "display_status": ["screen_visible"],
    "hardware_status": ["fan_noise", "overheating", "temperature"],
    "network_status": ["wifi_connected"]
}

print("=" * 55)
print("PART 1: KNOWLEDGE REPRESENTATION")
print("=" * 55)

print("\nKnowledge Base Facts:")
for fact, value in facts.items():
    print(f"- {fact}: {value}")

print("\nKnowledge Categories:")
for category, items in categories.items():
    print(f"- {category}: {', '.join(items)}")



# PART 2: RULE-BASED REASONING (RBR)


# Task 2A - Create at least 3 IF-THEN rules

def rule_power(facts):
    # IF the power cable is disconnected
    # THEN recommend connecting the power cable
    if not facts["power_connected"]:
        return "Connect the laptop to a power source."

    # IF the battery is not charged and the power light is off
    # THEN check the charger and power connection
    if not facts["battery_charged"] and not facts["power_light"]:
        return "Check the charger, power adapter, and battery."

    return None


def rule_display(facts):
    # IF the laptop has power but the screen is not visible
    # THEN troubleshoot the display
    if facts["power_light"] and not facts["screen_visible"]:
        return "Check the display brightness and external monitor."

    return None


def rule_overheating(facts):
    # IF the laptop is overheating
    # THEN improve cooling and check the ventilation
    if facts["overheating"] or facts["temperature"] >= 80:
        return "Clean the vents and allow the laptop to cool down."

    return None


def rule_wifi(facts):
    # IF Wi-Fi is disconnected
    # THEN check the wireless connection
    if not facts["wifi_connected"]:
        return "Check the Wi-Fi settings and reconnect to the network."

    return None


# Task 2B - Implement the Inference Engine
def inference_engine(facts):
    rules = [
        rule_power,
        rule_display,
        rule_overheating,
        rule_wifi
    ]

    actions = []

    # Check every rule against the knowledge base
    for rule in rules:
        result = rule(facts)
        if result is not None:
            actions.append(result)

    return actions


# Task 2C - Display RBR Output
print("\n" + "=" * 55)
print("PART 2: RULE-BASED REASONING (RBR)")
print("=" * 55)

rbr_actions = inference_engine(facts)

print("\nRule-Based Reasoning Actions:")

if rbr_actions:
    for action in rbr_actions:
        print(f"- {action}")
else:
    print("- No troubleshooting actions are needed.")



# PART 3: CASE-BASED REASONING (CBR)

# Task 3A - Build a Case Base

case_base = [
    {
        "problem": {
            "power_connected": False,
            "battery_charged": False,
            "power_light": False,
            "screen_visible": False,
            "fan_noise": False,
            "overheating": False,
            "wifi_connected": True
        },
        "solution": "Connect the power cable and check the adapter."
    },
    {
        "problem": {
            "power_connected": True,
            "battery_charged": True,
            "power_light": True,
            "screen_visible": False,
            "fan_noise": True,
            "overheating": False,
            "wifi_connected": True
        },
        "solution": "Check the screen brightness, display cable, or monitor."
    },
    {
        "problem": {
            "power_connected": True,
            "battery_charged": True,
            "power_light": True,
            "screen_visible": True,
            "fan_noise": True,
            "overheating": True,
            "wifi_connected": True
        },
        "solution": "Clean the cooling vents and check the laptop fan."
    },
    {
        "problem": {
            "power_connected": True,
            "battery_charged": True,
            "power_light": True,
            "screen_visible": True,
            "fan_noise": False,
            "overheating": False,
            "wifi_connected": False
        },
        "solution": "Enable Wi-Fi and reconnect to the network."
    }
]


# Task 3B - Retrieve the Most Similar Case
def calculate_similarity(new_problem, old_problem):
    # Count how many problem features match
    matching_features = 0

    for feature in new_problem:
        if new_problem[feature] == old_problem[feature]:
            matching_features += 1

    # Calculate similarity as a percentage
    total_features = len(new_problem)
    return matching_features / total_features


def retrieve_case(new_problem, case_base):
    best_case = None
    best_similarity = -1

    # Compare the new problem with every stored case
    for case in case_base:
        similarity = calculate_similarity(
            new_problem, case["problem"]
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_case = case

    return best_case, best_similarity


# Task 3C - Reuse the Retrieved Solution
# Task 3D - Revise the Solution
# Task 3E - Retain the New Case

print("\n" + "=" * 55)
print("PART 3: CASE-BASED REASONING (CBR)")
print("=" * 55)

print("\nStored Cases:", len(case_base))

print("\nEnter the current laptop symptoms.")
print("Answer using y for Yes or n for No.")

def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()

        if answer in ("y", "n"):
            return answer == "y"

        print("Invalid answer. Please enter y or n.")


# Gather a new problem from the user
new_problem = {
    "power_connected": ask_yes_no("Is the power cable connected?"),
    "battery_charged": ask_yes_no("Is the battery charged?"),
    "power_light": ask_yes_no("Is the power light on?"),
    "screen_visible": ask_yes_no("Is anything visible on the screen?"),
    "fan_noise": ask_yes_no("Can you hear the fan?"),
    "overheating": ask_yes_no("Is the laptop overheating?"),
    "wifi_connected": ask_yes_no("Is Wi-Fi connected?")
}

# RETRIEVE: Find the most similar past case
matched_case, similarity = retrieve_case(
    new_problem, case_base
)

print("\n--- 4R CYCLE ---")
print("\n1. RETRIEVE")
print("Most similar past case found.")
print(f"Similarity score: {similarity:.2%}")

# REUSE: Apply the past solution to the new problem
suggested_solution = matched_case["solution"]

print("\n2. REUSE")
print("Suggested solution:", suggested_solution)

# REVISE: Let the user accept or change the solution
print("\n3. REVISE")
print("You may accept the suggested solution or revise it.")

while True:
    choice = input(
        "Keep this solution? (y/n): "
    ).strip().lower()

    if choice in ("y", "n"):
        break

    print("Invalid answer. Please enter y or n.")

if choice == "y":
    final_solution = suggested_solution
    print("Solution accepted.")
else:
    final_solution = input(
        "Enter your revised troubleshooting solution: "
    ).strip()

    if not final_solution:
        final_solution = suggested_solution
        print("Empty solution. Original solution retained.")

# RETAIN: Save the new problem and its final solution
new_case = {
    "problem": new_problem.copy(),
    "solution": final_solution
}

case_base.append(new_case)

print("\n4. RETAIN")
print("The new problem and its solution were saved.")
print("Updated number of stored cases:", len(case_base))

print("\nFinal Recommended Solution:")
print(final_solution)

print("\n" + "=" * 55)
print("PROGRAM COMPLETED")
print("=" * 55)

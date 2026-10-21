#Task 1: Set Up the Environment:
def initialize_environment():
"""Allows the user to set the initial state (dirty or clean) for Rooms A and B."""
print("--- Set Initial State for Rooms ---")
env = {}
for room in ['A', 'B']:
state = input(f"Enter state for Room {room} (dirty/clean): ").strip().lower()
while state not in ['dirty', 'clean']:
state = input(f"Invalid input. Enter state for Room {room} (dirty/clean): ").strip().lower()
env[room] = state
return env
def is_dirty(env, room):
"""Checks if a specific room is dirty."""
return env[room] == 'dirty'
def clean_room(env, room):
"""Cleans a specific room by updating its state in the environment."""
env[room] = 'clean'

#Task 2: Implement the Rule-Based Agent:
class VacuumAgent:
def __init__(self, start_location='A'):
self.location = start_location
def perceive(self, env):
"""Perceives the state of the room the agent is currently in."""
return env[self.location]
def act(self, env):
"""
Decides an action based on rules:
- Rule 1: If current room is dirty, clean it.
- Rule 2: If current room is clean, move to the other room.
"""
percept = self.perceive(env)
if percept == 'dirty':
clean_room(env, self.location)
return "Cleaned the room"
else:
self.move()
return "Moved to the other room"
def move(self):
"""Switches the agent's location between Room A and Room B."""
if self.location == 'A':
    self.location = 'B'
else:
self.location = 'A'

#Task 3: Run the Simulation:
def run_simulation():
# Initialize environment
env = initialize_environment()
# Get user inputs for starting position and simulation steps
start_loc = input("Enter agent's starting location (A or B): ").strip().upper()
while start_loc not in ['A', 'B']:
start_loc = input("Invalid location. Enter starting location (A or B): ").strip().upper()
steps = int(input("Enter number of steps the simulation should run: "))
# Instantiate agent
agent = VacuumAgent(start_location=start_loc)
print(f"\nInitial Environment State: {env} | Agent Location: Room {agent.location}")
print("=" * 55)
# Run simulation loop
for step in range(1, steps + 1):
loc_before_action = agent.location
action_taken = agent.act(env)
print(f"Step {step}:")
print(f" - Agent's Current Location : Room {loc_before_action}")
print(f" - Action Taken : {action_taken}")
print(f" - Current Environment State: {env}")
print("-" * 55)
if __name__ == "__main__":
run_simulation()
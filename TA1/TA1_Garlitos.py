import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# -------- Get user input from console --------
    num_agents = int(input("Enter number of agents: "))
    grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
    num_steps = int(input("Enter number of steps: "))
    
# -------- Agent Definition -----------
    class RandomWalker(ap.Agent):
    def step(self):
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        x, y = self.position
# Keep agents inside grid
    x = max(0, min(self.model.p.grid_size[0]-1, x + direction[0]))
    y = max(0, min(self.model.p.grid_size[1]-1, y + direction[1]))
    self.position = (x, y)
    self.path.append(self.position)

# -------- Model Definition -----------
class RandomWalkModel(ap.Model):
    def setup(self):
# 1. Create agents
    self.agents = ap.AgentList(self, self.p.agents, RandomWalker)
# 2. Assign random positions and initialize path history BEFORE
    adding to grid
    for agent in self.agents:
    agent.position = (random.randint(0, self.p.grid_size[0]-1),
    random.randint(0, self.p.grid_size[1]-1))
agent.path = [agent.position]
# 3. Create grid and add agents
self.grid = ap.Grid(self, self.p.grid_size, torus=False)
self.grid.add_agents(self.agents)
def step(self):
for agent in self.agents:
agent.step()

# -------- Parameters from user input -----------
parameters = {
'agents': num_agents,
'grid_size': (grid_size, grid_size),
'steps': num_steps
}
# -------- Run Model -----------
model = RandomWalkModel(parameters)
model.setup()

# -------- Interactive Animation with Path Tracking -----------
fig, ax = plt.subplots()
ax.set_xlim(-0.5, model.p.grid_size[0] - 0.5)
ax.set_ylim(-0.5, model.p.grid_size[1] - 0.5)
ax.set_xticks(range(model.p.grid_size[0]))
ax.set_yticks(range(model.p.grid_size[1]))
ax.grid(True)

# Scatter plot for current positions and lines for paths
scat = ax.scatter([], [], s=100, color='red', zorder=3, label="Agents")
line_plots = [ax.plot([], [], lw=1.5, alpha=0.6)[0] for
_
range(model.p.agents)]
in
def update(frame):
model.step()

# Update current positions
    x = [agent.position[0] for agent in model.agents]
    y = [agent.position[1] for agent in model.agents]
    scat.set_offsets(list(zip(x, y)))
    
# Update trail/paths for each agent
for i, agent in enumerate(model.agents):
px = [pos[0] for pos in agent.path]
py = [pos[1] for pos in agent.path]
line_plots[i].set_data(px, py)
return [scat] + line_plots
ani = animation.FuncAnimation(fig, update, frames=model.p.steps,
interval=200, blit=False, repeat=False)
plt.title(f"Random Walk Simulation ({num_agents} Agents,
{grid_size}x{grid_size} Grid)")
plt.legend(loc='upper right')
plt.show()

# -------- Final Position Analysis Printout -----------
print("\n--- Final Positions of Agents ---")
for i, agent in enumerate(model.agents):
print(f"Agent {i+1} Final Position: {agent.position}")
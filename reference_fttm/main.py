import random
import matplotlib.pyplot as plt
import networkx as nx
from noc_simulator import NoC, Task
from fttm_mapper import FTTM_Mapper

def generate_random_tasks(num_tasks, max_partners=3):
    tasks = []
    for i in range(num_tasks):
        tasks.append(Task(i))
    
    # Add random dependencies
    for task in tasks:
        num_partners = random.randint(1, max_partners)
        for _ in range(num_partners):
            partner = random.choice(tasks)
            if partner != task:
                volume = random.randint(10, 100)
                task.add_dependency(partner.task_id, volume)
                # Symmetric communication for simplicity
                partner.add_dependency(task.task_id, volume)
    return tasks

def visualize_noc(noc, title="NoC Mapping"):
    """
    Visualizes the NoC grid and task mapping.
    """
    G = nx.grid_2d_graph(noc.width, noc.height)
    pos = {(x, y): (x, -y) for x, y in G.nodes()}
    
    plt.figure(figsize=(8, 8))
    
    # Draw nodes
    node_colors = []
    labels = {}
    for node in G.nodes():
        core = noc.get_core(node[0], node[1])
        if core.status == "FAULTY":
            node_colors.append('red')
            labels[node] = "FAULT"
        elif core.assigned_task:
            node_colors.append('lightgreen')
            labels[node] = f"T{core.assigned_task.task_id}"
        else:
            node_colors.append('lightgray')
            labels[node] = "Spare"

    nx.draw(G, pos, node_color=node_colors, with_labels=True, labels=labels, node_size=2000, font_weight='bold')
    # plt.show()
    filename = title.replace(" ", "_").replace(":", "").replace("(", "").replace(")", "") + ".png"
    plt.savefig(filename)
    print(f"Saved plot to {filename}")
    plt.close()

def main():
    # 1. Setup
    WIDTH = 4
    HEIGHT = 4
    NUM_TASKS = 12 # Leave some spares (16 cores total)
    
    print(f"--- Initializing {WIDTH}x{HEIGHT} NoC ---")
    noc = NoC(WIDTH, HEIGHT)
    mapper = FTTM_Mapper(noc)
    
    # 2. Generate Tasks
    print(f"--- Generating {NUM_TASKS} random tasks ---")
    tasks = generate_random_tasks(NUM_TASKS)
    
    # 3. Initial Mapping
    print("--- Performing Initial Mapping ---")
    mapper.initial_mapping(tasks)
    initial_energy = mapper.calculate_total_energy(tasks)
    print(f"Initial Total Energy: {initial_energy}")
    
    # Visualize Initial State
    print("Visualizing Initial State...")
    visualize_noc(noc, title=f"Initial Mapping (Energy: {initial_energy})")
    
    # 4. Inject Fault
    FAULT_X, FAULT_Y = 1, 1
    print(f"\n--- Injecting Permanent Fault at ({FAULT_X}, {FAULT_Y}) ---")
    mapper.handle_fault(FAULT_X, FAULT_Y)
    
    # 5. Post-Fault Analysis
    final_energy = mapper.calculate_total_energy(tasks)
    print(f"Post-Fault Total Energy: {final_energy}")
    print(f"Energy Overhead: {final_energy - initial_energy} (+{((final_energy - initial_energy)/initial_energy)*100:.2f}%)")
    
    # Visualize Final State
    print("Visualizing Post-Fault State...")
    visualize_noc(noc, title=f"Post-Fault Mapping (Energy: {final_energy})")

if __name__ == "__main__":
    main()

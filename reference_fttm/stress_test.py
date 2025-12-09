import random
import matplotlib.pyplot as plt
import networkx as nx
from noc_simulator import NoC, Task
from fttm_mapper import FTTM_Mapper
from main import generate_random_tasks, visualize_noc

def main():
    print("=== NoC Stress Test: Multiple Faults ===")
    
    # 1. Setup
    WIDTH = 5
    HEIGHT = 5
    NUM_TASKS = 15
    noc = NoC(WIDTH, HEIGHT)
    mapper = FTTM_Mapper(noc)
    
    # 2. Generate Tasks
    tasks = generate_random_tasks(NUM_TASKS)
    mapper.initial_mapping(tasks)
    
    base_energy = mapper.calculate_total_energy(tasks)
    print(f"Initial Energy: {base_energy}")
    visualize_noc(noc, title=f"Stress Test - Initial (E={base_energy})")
    
    # 3. Inject Multiple Faults
    faults_to_inject = 3
    for i in range(faults_to_inject):
        # Pick a random core that has a task
        occupied_cores = [c for c in noc.cores.values() if c.assigned_task and c.status == "HEALTHY"]
        if not occupied_cores:
            print("No more occupied cores to fault!")
            break
            
        target = random.choice(occupied_cores)
        print(f"\n--- Injecting Fault #{i+1} at Core {target.core_id} ({target.x}, {target.y}) ---")
        
        mapper.handle_fault(target.x, target.y)
        
        current_energy = mapper.calculate_total_energy(tasks)
        overhead = ((current_energy - base_energy) / base_energy) * 100
        print(f"Current Energy: {current_energy} (Overhead: {overhead:.2f}%)")
        
        visualize_noc(noc, title=f"Stress Test - Fault {i+1} (E={current_energy})")

    print("\n=== Stress Test Completed ===")

if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import random
import numpy as np
from noc_simulator import NoC, Task
from fttm_mapper import FTTM_Mapper
from main import generate_random_tasks

class Random_Mapper:
    def __init__(self, noc):
        self.noc = noc
        self.task_map = {}

    def map_tasks(self, tasks):
        available_cores = self.noc.get_available_cores()
        random.shuffle(available_cores)
        
        for i, task in enumerate(tasks):
            if i < len(available_cores):
                core = available_cores[i]
                core.assign_task(task)
                self.task_map[task.task_id] = core.core_id

    def calculate_total_energy(self, tasks):
        # Reusing the logic from FTTM_Mapper for consistency, 
        # but we need to instantiate it or copy the logic. 
        # Let's just use FTTM_Mapper's method by temporarily creating one or making it static.
        # Easier: just implement the simple sum here.
        total_energy = 0
        for task in tasks:
            core_id = self.task_map.get(task.task_id)
            if core_id is not None:
                core = self.noc.get_core_by_id(core_id)
                for partner_id, volume in task.communication_partners.items():
                    partner_core_id = self.task_map.get(partner_id)
                    if partner_core_id is not None:
                        partner_core = self.noc.get_core_by_id(partner_core_id)
                        hops = self.noc.get_manhattan_distance(core, partner_core)
                        total_energy += volume * hops
        return total_energy

def run_comparison():
    print("=== Running FTTM vs Random Mapping Comparison ===")
    
    WIDTH = 4
    HEIGHT = 4
    NUM_TASKS = 12
    ITERATIONS = 5 # Average over multiple runs to be fair
    
    fttm_energies = []
    random_energies = []
    
    for i in range(ITERATIONS):
        # 1. Setup Environment
        noc_fttm = NoC(WIDTH, HEIGHT)
        noc_rnd = NoC(WIDTH, HEIGHT)
        
        tasks = generate_random_tasks(NUM_TASKS)
        
        # 2. Run FTTM
        mapper_fttm = FTTM_Mapper(noc_fttm)
        mapper_fttm.initial_mapping(tasks)
        e_fttm = mapper_fttm.calculate_total_energy(tasks)
        fttm_energies.append(e_fttm)
        
        # 3. Run Random
        mapper_rnd = Random_Mapper(noc_rnd)
        mapper_rnd.map_tasks(tasks)
        e_rnd = mapper_rnd.calculate_total_energy(tasks)
        random_energies.append(e_rnd)
        
        print(f"Run {i+1}: FTTM={e_fttm}, Random={e_rnd}")

    avg_fttm = np.mean(fttm_energies)
    avg_rnd = np.mean(random_energies)
    improvement = ((avg_rnd - avg_fttm) / avg_rnd) * 100
    
    print(f"\nAverage FTTM Energy: {avg_fttm:.2f}")
    print(f"Average Random Energy: {avg_rnd:.2f}")
    print(f"Improvement: {improvement:.2f}%")
    
    # Plotting
    labels = ['FTTM (Proposed)', 'Random Mapping']
    means = [avg_fttm, avg_rnd]
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, means, color=['green', 'gray'])
    plt.ylabel('Total Communication Energy')
    plt.title(f'Energy Efficiency Comparison (Avg of {ITERATIONS} runs)')
    plt.text(0, avg_fttm, f"{avg_fttm:.0f}", ha='center', va='bottom')
    plt.text(1, avg_rnd, f"{avg_rnd:.0f}", ha='center', va='bottom')
    
    filename = "Comparison_FTTM_vs_Random.png"
    plt.savefig(filename)
    print(f"Saved comparison plot to {filename}")

if __name__ == "__main__":
    run_comparison()

import random
from noc_simulator import NoC, Task, Core

class FTTM_Mapper:
    def __init__(self, noc: NoC):
        self.noc = noc
        self.task_map = {} # task_id -> core_id

    def initial_mapping(self, tasks):
        """
        Maps tasks to cores.
        Simple strategy: Map tasks sequentially to available healthy cores.
        In a real scenario, this would be an optimization problem (e.g., Simulated Annealing).
        """
        available_cores = self.noc.get_available_cores()
        if len(available_cores) < len(tasks):
            raise RuntimeError("Not enough healthy cores for tasks")

        # Sort tasks by connectivity (heuristic: map highly connected tasks first)
        # For now, just simple sequential mapping
        for i, task in enumerate(tasks):
            core = available_cores[i]
            core.assign_task(task)
            self.task_map[task.task_id] = core.core_id
        
        print(f"Initial mapping completed for {len(tasks)} tasks.")

    def handle_fault(self, faulty_core_x, faulty_core_y):
        """
        Handles a permanent fault at (x, y).
        Remaps the task from the faulty core to the best available spare core.
        """
        faulty_core = self.noc.get_core(faulty_core_x, faulty_core_y)
        if not faulty_core:
            return
        
        task_to_move = faulty_core.assigned_task
        
        # Mark core as faulty (this clears the assigned task in the core object logic if we were strict, 
        # but here we need to hold onto the task first)
        faulty_core.set_faulty() 
        
        if task_to_move:
            print(f"Task {task_to_move.task_id} displaced from Core {faulty_core.core_id}. Finding spare...")
            new_core = self._find_best_spare_core(task_to_move)
            if new_core:
                new_core.assign_task(task_to_move)
                self.task_map[task_to_move.task_id] = new_core.core_id
                print(f"Task {task_to_move.task_id} remapped to Core {new_core.core_id} ({new_core.x}, {new_core.y})")
            else:
                print(f"CRITICAL: No spare cores available for Task {task_to_move.task_id}!")

    def _find_best_spare_core(self, task):
        """
        Finds the spare core that minimizes the increase in communication cost.
        """
        spares = self.noc.get_available_cores()
        if not spares:
            return None

        best_core = None
        min_energy_impact = float('inf')

        for spare in spares:
            energy = self._calculate_task_energy_on_core(task, spare)
            if energy < min_energy_impact:
                min_energy_impact = energy
                best_core = spare
        
        return best_core

    def _calculate_task_energy_on_core(self, task, core):
        """
        Calculates the communication energy for a specific task if it were placed on 'core'.
        """
        energy = 0
        for partner_id, volume in task.communication_partners.items():
            partner_core_id = self.task_map.get(partner_id)
            if partner_core_id is not None:
                partner_core = self.noc.get_core_by_id(partner_core_id)
                # If partner is on a faulty core (and hasn't been moved yet), this might be inaccurate,
                # but we assume sequential fault handling or that partners are active.
                if partner_core and partner_core.status == "HEALTHY":
                    hops = self.noc.get_manhattan_distance(core, partner_core)
                    energy += volume * hops
        return energy

    def calculate_total_energy(self, tasks):
        """
        Calculates the total communication energy of the current mapping.
        """
        total_energy = 0
        for task in tasks:
            core_id = self.task_map.get(task.task_id)
            if core_id is not None:
                core = self.noc.get_core_by_id(core_id)
                total_energy += self._calculate_task_energy_on_core(task, core)
        # Note: This double counts each link (A->B and B->A). 
        # If the graph is undirected, divide by 2. If directed, it's correct.
        # Assuming undirected communication volume for simplicity, we can divide by 2 or keep as is for relative comparison.
        return total_energy

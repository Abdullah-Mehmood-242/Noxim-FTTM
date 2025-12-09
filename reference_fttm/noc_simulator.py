import networkx as nx
import math

class Task:
    def __init__(self, task_id, instruction_count=1000):
        self.task_id = task_id
        self.instruction_count = instruction_count
        self.communication_partners = {} # {partner_task_id: volume_in_bits}

    def add_dependency(self, partner_id, volume):
        self.communication_partners[partner_id] = volume

    def __repr__(self):
        return f"Task({self.task_id})"

class Core:
    def __init__(self, core_id, x, y):
        self.core_id = core_id
        self.x = x
        self.y = y
        self.status = "HEALTHY" # "HEALTHY" or "FAULTY"
        self.assigned_task = None

    def set_faulty(self):
        self.status = "FAULTY"
        self.assigned_task = None

    def assign_task(self, task):
        if self.status == "FAULTY":
            raise RuntimeError(f"Cannot assign task to faulty core {self.core_id}")
        self.assigned_task = task

    def free_task(self):
        self.assigned_task = None

    def __repr__(self):
        return f"Core({self.core_id} @ {self.x},{self.y} [{self.status}])"

class NoC:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cores = {} # (x, y) -> Core
        self.graph = nx.grid_2d_graph(width, height)
        self._initialize_cores()

    def _initialize_cores(self):
        id_counter = 0
        for y in range(self.height):
            for x in range(self.width):
                self.cores[(x, y)] = Core(id_counter, x, y)
                id_counter += 1

    def get_core(self, x, y):
        return self.cores.get((x, y))

    def get_core_by_id(self, core_id):
        for core in self.cores.values():
            if core.core_id == core_id:
                return core
        return None

    def get_manhattan_distance(self, core1, core2):
        return abs(core1.x - core2.x) + abs(core1.y - core2.y)

    def inject_permanent_fault(self, x, y):
        core = self.get_core(x, y)
        if core:
            core.set_faulty()
            print(f"Fault injected at Core {core.core_id} ({x}, {y})")

    def get_available_cores(self):
        return [c for c in self.cores.values() if c.status == "HEALTHY" and c.assigned_task is None]

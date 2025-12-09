import unittest
from noc_simulator import NoC, Core, Task
from fttm_mapper import FTTM_Mapper

class TestNoCSimulator(unittest.TestCase):
    def setUp(self):
        self.noc = NoC(4, 4)
        self.mapper = FTTM_Mapper(self.noc)

    def test_noc_initialization(self):
        """Test if NoC is initialized with correct number of cores."""
        self.assertEqual(len(self.noc.cores), 16)
        core = self.noc.get_core(0, 0)
        self.assertIsNotNone(core)
        self.assertEqual(core.status, "HEALTHY")

    def test_task_assignment(self):
        """Test if a task can be assigned to a core."""
        core = self.noc.get_core(0, 0)
        task = Task(1)
        core.assign_task(task)
        self.assertEqual(core.assigned_task, task)

    def test_fault_injection(self):
        """Test if fault injection works."""
        self.noc.inject_permanent_fault(1, 1)
        core = self.noc.get_core(1, 1)
        self.assertEqual(core.status, "FAULTY")

    def test_fttm_mapping(self):
        """Test if FTTM maps tasks correctly."""
        tasks = [Task(i) for i in range(5)]
        self.mapper.initial_mapping(tasks)
        
        # Check if all tasks are mapped
        self.assertEqual(len(self.mapper.task_map), 5)
        
        # Check if mapped to healthy cores
        for task_id, core_id in self.mapper.task_map.items():
            core = self.noc.get_core_by_id(core_id)
            self.assertEqual(core.status, "HEALTHY")

    def test_fault_recovery(self):
        """Test if FTTM recovers from a fault."""
        task = Task(99)
        core = self.noc.get_core(2, 2)
        core.assign_task(task)
        self.mapper.task_map[99] = core.core_id
        
        # Inject fault
        self.mapper.handle_fault(2, 2)
        
        # Check if task was moved
        new_core_id = self.mapper.task_map[99]
        new_core = self.noc.get_core_by_id(new_core_id)
        
        self.assertNotEqual(new_core.core_id, core.core_id)
        self.assertEqual(new_core.status, "HEALTHY")
        self.assertEqual(new_core.assigned_task, task)

if __name__ == '__main__':
    unittest.main()

#ifndef __NOXIMMANAGERCORE_H__
#define __NOXIMMANAGERCORE_H__

#include <vector>
#include <map>
#include "DataStructs.h"

using namespace std;

// Forward declaration to avoid circular dependency
class NoC;

class NoximManagerCore {
public:
    NoximManagerCore(NoC* noc);

    // Core FTTM Methods
    void initialMapping(vector<Task>& tasks);
    void handleFault(int faulty_core_x, int faulty_core_y);
    void injectFault(int x, int y);
    
    // Accessors
    int getTaskLocation(int task_id);
    CoreStatus getCoreStatus(int x, int y);

    // Visualization Support
    void dumpState(string title);

private:
    NoC* noc;
    map<int, int> task_map; // task_id -> core_id (linear index)
    map<int, CoreStatus> core_status; // core_id -> status

    // Helper Methods
    int findBestSpareCore(int task_id);
    double calculateTaskEnergyOnCore(const Task& task, int core_id);
    int getManhattanDistance(int core_id1, int core_id2);
    
    // Internal state
    vector<Task> all_tasks;
};

#endif

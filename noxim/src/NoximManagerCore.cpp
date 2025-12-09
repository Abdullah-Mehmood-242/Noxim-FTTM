#include "NoximManagerCore.h"
#include "NoC.h"
#include "GlobalParams.h"
#include <cmath>
#include <algorithm>
#include <iostream>
#include <fstream>

NoximManagerCore::NoximManagerCore(NoC* _noc) : noc(_noc) {
    // Initialize core status
    int total_cores = GlobalParams::mesh_dim_x * GlobalParams::mesh_dim_y;
    for (int i = 0; i < total_cores; i++) {
        core_status[i] = CORE_HEALTHY;
    }
}

void NoximManagerCore::initialMapping(vector<Task>& tasks) {
    all_tasks = tasks;
    int width = GlobalParams::mesh_dim_x;
    int height = GlobalParams::mesh_dim_y;
    
    // Simple sequential mapping for now, as per reference code placeholder
    // In a full implementation, this would use the OD algorithm
    // "Map tasks sequentially to available healthy cores"
    
    int core_idx = 0;
    for (const auto& task : tasks) {
        if (core_idx >= width * height) {
            cerr << "Error: Not enough cores for tasks!" << endl;
            break;
        }
        
        // Find next healthy core
        while (core_status[core_idx] != CORE_HEALTHY && core_idx < width * height) {
            core_idx++;
        }
        
        if (core_idx < width * height) {
            task_map[task.task_id] = core_idx;
            core_status[core_idx] = CORE_BUSY;
            cout << "Mapped Task " << task.task_id << " to Core " << core_idx << endl;
            core_idx++;
        }
    }
}

void NoximManagerCore::injectFault(int x, int y) {
    int core_id = y * GlobalParams::mesh_dim_x + x;
    if (core_status.find(core_id) != core_status.end()) {
        core_status[core_id] = CORE_FAULTY;
        cout << "Fault injected at Core " << core_id << " (" << x << "," << y << ")" << endl;
        handleFault(x, y);
    }
}

void NoximManagerCore::handleFault(int faulty_core_x, int faulty_core_y) {
    int faulty_core_id = faulty_core_y * GlobalParams::mesh_dim_x + faulty_core_x;
    
    // Find if any task was mapped here
    int task_to_move = -1;
    for (auto const& [task_id, core_id] : task_map) {
        if (core_id == faulty_core_id) {
            task_to_move = task_id;
            break;
        }
    }
    
    if (task_to_move != -1) {
        cout << "Task " << task_to_move << " displaced from Core " << faulty_core_id << ". Finding spare..." << endl;
        int new_core_id = findBestSpareCore(task_to_move);
        
        if (new_core_id != -1) {
            task_map[task_to_move] = new_core_id;
            core_status[new_core_id] = CORE_BUSY; // Or keep as SPARE/BUSY
            cout << "Task " << task_to_move << " remapped to Core " << new_core_id << endl;
        } else {
            cerr << "CRITICAL: No spare cores available for Task " << task_to_move << "!" << endl;
        }
    }
}

int NoximManagerCore::findBestSpareCore(int task_id) {
    int best_core = -1;
    double min_energy = 1e9; // Infinity
    
    // Find the task object
    Task current_task;
    bool found = false;
    for(const auto& t : all_tasks) {
        if(t.task_id == task_id) {
            current_task = t;
            found = true;
            break;
        }
    }
    if(!found) return -1;

    int total_cores = GlobalParams::mesh_dim_x * GlobalParams::mesh_dim_y;
    for (int i = 0; i < total_cores; i++) {
        if (core_status[i] == CORE_HEALTHY) { // Assuming HEALTHY means free/spare for now
             // In a real scenario, we distinguish FREE vs BUSY. 
             // Here, initialMapping marks BUSY. So HEALTHY means FREE.
             
             double energy = calculateTaskEnergyOnCore(current_task, i);
             if (energy < min_energy) {
                 min_energy = energy;
                 best_core = i;
             }
        }
    }
    return best_core;
}

double NoximManagerCore::calculateTaskEnergyOnCore(const Task& task, int core_id) {
    double energy = 0;
    for (auto const& [partner_id, volume] : task.communication_partners) {
        if (task_map.find(partner_id) != task_map.end()) {
            int partner_core_id = task_map[partner_id];
            // Check if partner is not on a faulty core (unless it's the one being moved, which is impossible here)
            if (core_status[partner_core_id] != CORE_FAULTY) {
                int hops = getManhattanDistance(core_id, partner_core_id);
                energy += volume * hops;
            }
        }
    }
    return energy;
}

int NoximManagerCore::getManhattanDistance(int core_id1, int core_id2) {
    int width = GlobalParams::mesh_dim_x;
    int x1 = core_id1 % width;
    int y1 = core_id1 / width;
    int x2 = core_id2 % width;
    int y2 = core_id2 / width;
    
    return abs(x1 - x2) + abs(y1 - y2);
}

int NoximManagerCore::getTaskLocation(int task_id) {
    if (task_map.find(task_id) != task_map.end()) {
        return task_map[task_id];
    }
    return -1;
}

CoreStatus NoximManagerCore::getCoreStatus(int x, int y) {
    int id = y * GlobalParams::mesh_dim_x + x;
    if (core_status.find(id) != core_status.end()) {
        return core_status[id];
    }
    return CORE_FAULTY; // Default to faulty if out of bounds
}

void NoximManagerCore::dumpState(string title) {
    ofstream out_file;
    // Open in append mode
    out_file.open("noxim_state.json", ios_base::app);
    
    if (!out_file.is_open()) {
        cout << "Error opening noxim_state.json" << endl;
        return;
    }

    // If file is empty, start the JSON array
    out_file.seekp(0, ios::end);
    if (out_file.tellp() == 0) {
        out_file << "[" << endl;
    } else {
        // If not empty, add a comma before the new object
        out_file << "," << endl;
    }

    out_file << "  {" << endl;
    out_file << "    \"title\": \"" << title << "\"," << endl;
    out_file << "    \"width\": " << GlobalParams::mesh_dim_x << "," << endl;
    out_file << "    \"height\": " << GlobalParams::mesh_dim_y << "," << endl;
    
    // Calculate total energy for this snapshot
    double total_energy = 0;
    for (const auto& task : all_tasks) {
        int core_id = getTaskLocation(task.task_id);
        if (core_id != -1) {
             total_energy += calculateTaskEnergyOnCore(task, core_id);
        }
    }
    out_file << "    \"total_energy\": " << total_energy << "," << endl;

    out_file << "    \"cores\": [" << endl;
    
    for (int y = 0; y < GlobalParams::mesh_dim_y; y++) {
        for (int x = 0; x < GlobalParams::mesh_dim_x; x++) {
            int id = y * GlobalParams::mesh_dim_x + x;
            
            out_file << "      {" << endl;
            out_file << "        \"id\": " << id << "," << endl;
            out_file << "        \"x\": " << x << "," << endl;
            out_file << "        \"y\": " << y << "," << endl;
            
            string status_str = "HEALTHY";
            if (core_status[id] == CORE_FAULTY) status_str = "FAULTY";
            else if (core_status[id] == CORE_BUSY) status_str = "BUSY";
            else if (core_status[id] == CORE_SPARE) status_str = "SPARE";
            
            out_file << "        \"status\": \"" << status_str << "\"," << endl;
            
            // Check if a task is mapped here
            int mapped_task_id = -1;
            for(auto const& [tid, cid] : task_map) {
                if(cid == id) {
                    mapped_task_id = tid;
                    break;
                }
            }

            if (mapped_task_id != -1) {
                out_file << "        \"task_id\": " << mapped_task_id << endl;
            } else {
                out_file << "        \"task_id\": null" << endl;
            }
            
            if (id == (GlobalParams::mesh_dim_x * GlobalParams::mesh_dim_y) - 1) {
                out_file << "      }" << endl;
            } else {
                out_file << "      }," << endl;
            }
        }
    }
    out_file << "    ]" << endl;
    out_file << "  }"; // End of snapshot object
    
    out_file.close();
}

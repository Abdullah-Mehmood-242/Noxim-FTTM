import json
import matplotlib.pyplot as plt
import networkx as nx
import os

def visualize_snapshot(snapshot, filename):
    width = snapshot['width']
    height = snapshot['height']
    title = snapshot['title']
    total_energy = snapshot['total_energy']
    cores = snapshot['cores']

    print(f"Generating plot for: {title} (Energy: {total_energy})")

    G = nx.grid_2d_graph(width, height)
    # Flip y-axis for visualization so (0,0) is top-left or bottom-left as preferred.
    # Noxim usually has (0,0) top-left. Let's match standard matrix layout.
    pos = {(x, y): (x, -y) for x, y in G.nodes()}

    node_colors = []
    labels = {}
    
    # Create a map for easy lookup
    core_map = {}
    for core in cores:
        core_map[(core['x'], core['y'])] = core

    for node in G.nodes():
        x, y = node
        if (x, y) in core_map:
            core = core_map[(x, y)]
            status = core['status']
            task_id = core['task_id']
            
            if status == "FAULTY":
                node_colors.append('red')
                labels[node] = "FAULT"
            elif task_id is not None:
                node_colors.append('lightgreen')
                labels[node] = f"T{task_id}"
            elif status == "BUSY": # Should be covered by task_id check, but just in case
                node_colors.append('orange')
                labels[node] = "BUSY"
            else:
                node_colors.append('lightgray')
                labels[node] = "Spare"
        else:
            node_colors.append('white')
            labels[node] = "?"

    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_color=node_colors, with_labels=True, labels=labels, node_size=2000, font_weight='bold', edge_color='gray')
    plt.title(f"{title}\nTotal Energy: {total_energy:.2f}")
    
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")

def main():
    json_file = "noxim_state.json"
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found. Run ./noxim first.")
        return

    with open(json_file, 'r') as f:
        # The file might contain multiple JSON objects if not formatted as a single array properly
        # But my C++ code tries to format it as an array.
        # However, if the file was appended to multiple times across runs without clearing, it might be malformed.
        # Let's assume a clean run.
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON. Trying to fix common issues...")
            # Fallback: read line by line or handle trailing commas if necessary
            # For now, assume valid JSON from the C++ dumper.
            return

    # Data should be a list of snapshots
    if isinstance(data, list):
        for i, snapshot in enumerate(data):
            safe_title = snapshot['title'].replace(" ", "_").replace(":", "")
            filename = f"{safe_title}.png"
            visualize_snapshot(snapshot, filename)
    
    # Generate Comparison Graph if we have at least 2 snapshots
    if len(data) >= 2:
        titles = [s['title'] for s in data]
        energies = [s['total_energy'] for s in data]
        
        plt.figure(figsize=(10, 6))
        plt.bar(titles, energies, color=['green', 'orange', 'red'][:len(data)])
        plt.ylabel('Total Communication Energy')
        plt.title('Energy Comparison')
        for i, v in enumerate(energies):
            plt.text(i, v, f"{v:.1f}", ha='center', va='bottom')
        
        plt.savefig("Energy_Comparison.png")
        print("Saved Energy_Comparison.png")

if __name__ == "__main__":
    main()

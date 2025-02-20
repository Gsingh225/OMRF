import matplotlib.pyplot as plt
import re
from collections import deque
import math

def parse_molecule(input_str):
    """Parse the input string into a dictionary of atoms and connections."""
    atoms = {}
    for line in input_str.split(';'):
        line = line.strip()
        if not line:
            continue
        match = re.match(r'(\w+)(\{.*?\})?\[(.*)\]', line)
        if match:
            atom_label = match.group(1)
            charge = match.group(2) if match.group(2) else ''
            connections_str = match.group(3)
            connections = []
            for conn in connections_str.split(','):
                conn = conn.strip()
                if conn.endswith('::'):
                    direction = conn[:-2]
                    connections.append((direction, 'lone_pair'))
                else:
                    direction, bond_type, connected_atom = conn.split(':')
                    connections.append((direction, bond_type, connected_atom))
            atoms[atom_label] = {'charge': charge, 'connections': connections}
    return atoms

def build_graph(atoms):
    """Build an adjacency list representation of the molecule's connectivity."""
    graph = {}
    for atom in atoms:
        neighbors = [conn[2] for conn in atoms[atom]['connections'] if len(conn) == 3]
        graph[atom] = neighbors
    return graph

def find_cycle(graph):
    """Find a cycle in the graph using DFS."""
    def dfs(node, parent, path, visited):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            if neighbor in visited:
                cycle_start = path.index(neighbor)
                return path[cycle_start:]
            path.append(neighbor)
            result = dfs(neighbor, node, path, visited)
            if result:
                return result
            path.pop()
        return None

    visited = set()
    for node in graph:
        if node not in visited:
            cycle = dfs(node, None, [node], visited)
            if cycle:
                return cycle
    return None

def place_atoms(atoms):
    """Place atoms on a 2D grid, handling cyclic structures with a circular layout."""
    graph = build_graph(atoms)
    cycle = find_cycle(graph)
    positions = {}

    if cycle:
        # Place atoms in the cycle in a circular layout
        n = len(cycle)
        radius = 1.0  # Adjust radius for visibility
        for i, atom in enumerate(cycle):
            angle = 2 * math.pi * i / n
            pos = (radius * math.cos(angle), radius * math.sin(angle))
            positions[atom] = pos
    else:
        # No cycle; use grid-based placement
        start_atom = next(iter(atoms))
        positions[start_atom] = (0, 0)

    # Use BFS to place remaining atoms
    queue = deque(positions.keys())
    while queue:
        current = queue.popleft()
        current_pos = positions[current]
        for connection in atoms[current]['connections']:
            if len(connection) != 3:  # Skip lone pairs
                continue
            direction, bond_type, connected_atom = connection
            if connected_atom in positions:
                continue

            # Special handling for atoms connected to the cycle
            if cycle and current in cycle and direction == 'above':
                # Place hydrogen outward from the ring center (assumed at (0,0))
                vec = positions[current]
                norm = math.sqrt(vec[0]**2 + vec[1]**2)
                if norm > 0:
                    unit_vec = (vec[0]/norm, vec[1]/norm)
                    pos = (current_pos[0] + unit_vec[0], current_pos[1] + unit_vec[1])
                else:
                    pos = (current_pos[0], current_pos[1] + 1)  # Default
            else:
                # Standard grid placement
                if direction == 'right':
                    pos = (current_pos[0] + 1, current_pos[1])
                elif direction == 'left':
                    pos = (current_pos[0] - 1, current_pos[1])
                elif direction == 'above':
                    pos = (current_pos[0], current_pos[1] + 1)
                elif direction == 'below':
                    pos = (current_pos[0], current_pos[1] - 1)
                else:
                    raise ValueError(f"Unknown direction: {direction}")
            
            positions[connected_atom] = pos
            queue.append(connected_atom)

    return positions

def draw_molecule(atoms, positions, padding=0.2, double_bond_offset=0.1):
    """Draw the molecule with padding between atoms and bonds."""
    # Set up the figure size based on molecule extent
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]
    x_range = max(all_x) - min(all_x) + 2
    y_range = max(all_y) - min(all_y) + 2
    fig, ax = plt.subplots(figsize=(max(6, x_range), max(4, y_range)))
    ax.set_aspect('equal')

    # Draw atoms
    for atom, pos in positions.items():
        label = atom[0]  # Element symbol
        if atoms[atom]['charge']:
            label += atoms[atom]['charge']
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontsize=14, fontweight='bold')

    # Draw bonds with padding
    drawn_bonds = set()
    for atom, data in atoms.items():
        pos1 = positions[atom]
        for connection in data['connections']:
            if len(connection) == 3:  # Bond
                direction, bond_type, connected_atom = connection
                bond = frozenset([atom, connected_atom])
                if bond in drawn_bonds:
                    continue
                drawn_bonds.add(bond)
                pos2 = positions[connected_atom]
                vec = (pos2[0] - pos1[0], pos2[1] - pos1[1])
                start = (pos1[0] + padding * vec[0], pos1[1] + padding * vec[1])
                end = (pos2[0] - padding * vec[0], pos2[1] - padding * vec[1])
                
                if bond_type == '-':
                    ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2)
                elif bond_type == '=':
                    perp_vec = (-vec[1], vec[0])
                    start1 = (start[0] + double_bond_offset * perp_vec[0], start[1] + double_bond_offset * perp_vec[1])
                    end1 = (end[0] + double_bond_offset * perp_vec[0], end[1] + double_bond_offset * perp_vec[1])
                    ax.plot([start1[0], end1[0]], [start1[1], end1[1]], 'k-', linewidth=2)
                    start2 = (start[0] - double_bond_offset * perp_vec[0], start[1] - double_bond_offset * perp_vec[1])
                    end2 = (end[0] - double_bond_offset * perp_vec[0], end[1] - double_bond_offset * perp_vec[1])
                    ax.plot([start2[0], end2[0]], [start2[1], end2[1]], 'k-', linewidth=2)
                elif bond_type == '≡':
                    ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2)
                    perp_vec = (-vec[1], vec[0])
                    start1 = (start[0] + double_bond_offset * perp_vec[0], start[1] + double_bond_offset * perp_vec[1])
                    end1 = (end[0] + double_bond_offset * perp_vec[0], end[1] + double_bond_offset * perp_vec[1])
                    ax.plot([start1[0], end1[0]], [start1[1], end1[1]], 'k-', linewidth=2)
                    start2 = (start[0] - double_bond_offset * perp_vec[0], start[1] - double_bond_offset * perp_vec[1])
                    end2 = (end[0] - double_bond_offset * perp_vec[0], end[1] - double_bond_offset * perp_vec[1])
                    ax.plot([start2[0], end2[0]], [start2[1], end2[1]], 'k-', linewidth=2)

    # Draw lone pairs
    for atom, data in atoms.items():
        pos = positions[atom]
        for connection in data['connections']:
            if len(connection) == 2:  # Lone pair
                direction, _ = connection
                if direction == 'right':
                    lp1 = (pos[0] + 0.2, pos[1])
                    lp2 = (pos[0] + 0.4, pos[1])
                elif direction == 'left':
                    lp1 = (pos[0] - 0.2, pos[1])
                    lp2 = (pos[0] - 0.4, pos[1])
                elif direction == 'above':
                    lp1 = (pos[0], pos[1] + 0.2)
                    lp2 = (pos[0], pos[1] + 0.4)
                elif direction == 'below':
                    lp1 = (pos[0], pos[1] - 0.2)
                    lp2 = (pos[0], pos[1] - 0.4)
                ax.plot([lp1[0]], [lp1[1]], 'ko', markersize=6)
                ax.plot([lp2[0]], [lp2[1]], 'ko', markersize=6)

    # Adjust plot limits
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]
    for atom, data in atoms.items():
        pos = positions[atom]
        for connection in data['connections']:
            if len(connection) == 2:
                direction, _ = connection
                if direction == 'right':
                    all_x.append(pos[0] + 0.5)
                elif direction == 'left':
                    all_x.append(pos[0] - 0.5)
                elif direction == 'above':
                    all_y.append(pos[1] + 0.5)
                elif direction == 'below':
                    all_y.append(pos[1] - 0.5)
    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
    ax.axis('off')
    plt.title("Lewis Structure")
    plt.show()

# Test with Benzene
input_str = ("C1[right:=:C2, left:=:C6, above:-:H1];"
             "C2[right:-:C3, left:=:C1, above:-:H2];"
             "C3[right:=:C4, left:-:C2, above:-:H3];"
             "C4[right:-:C5, left:=:C3, above:-:H4];"
             "C5[right:=:C6, left:-:C4, above:-:H5];"
             "C6[right:-:C1, left:=:C5, above:-:H6];"
             "H1[below:-:C1];H2[below:-:C2];H3[below:-:C3];"
             "H4[below:-:C4];H5[below:-:C5];H6[below:-:C6]")
atoms_benzene = parse_molecule(input_str)
positions_benzene = place_atoms(atoms_benzene)
draw_molecule(atoms_benzene, positions_benzene)

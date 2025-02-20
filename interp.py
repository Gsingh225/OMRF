import matplotlib.pyplot as plt
import re
from collections import deque

def parse_molecule(input_str):
    """Parse the molecular input into a dictionary of atoms and their connections."""
    atoms = {}
    for line in input_str.split(';'):
        line = line.strip()
        if not line:
            continue
        # Match format: Atom_label{charge}[connection1, connection2, ...]
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

def place_atoms(atoms):
    """Assign 2D grid positions to atoms based on connection directions."""
    positions = {}
    queue = deque()
    # Start with the first atom at (0,0)
    start_atom = next(iter(atoms))
    positions[start_atom] = (0, 0)
    queue.append(start_atom)

    while queue:
        current = queue.popleft()
        current_pos = positions[current]
        for connection in atoms[current]['connections']:
            if len(connection) == 2:  # lone pair
                continue
            direction, bond_type, connected_atom = connection
            if connected_atom in positions:
                continue  # Skip if already placed
            # Assign position based on direction
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

def draw_molecule(atoms, positions):
    """Draw the Lewis structure using Matplotlib."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')

    # Draw atoms
    for atom, pos in positions.items():
        label = atom[0]  # Use element symbol (e.g., 'N' from 'N1')
        if atoms[atom]['charge']:
            label += atoms[atom]['charge']  # Append charge if present
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontsize=12)

    # Draw bonds
    drawn_bonds = set()
    for atom, data in atoms.items():
        pos1 = positions[atom]
        for connection in data['connections']:
            if len(connection) == 3:  # bond
                direction, bond_type, connected_atom = connection
                bond = frozenset([atom, connected_atom])
                if bond in drawn_bonds:
                    continue
                drawn_bonds.add(bond)
                pos2 = positions[connected_atom]
                dx = pos2[0] - pos1[0]
                dy = pos2[1] - pos1[1]
                if bond_type == '-':
                    ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 'k-')
                elif bond_type == '=':
                    if dx != 0:  # horizontal
                        ax.plot([pos1[0], pos2[0]], [pos1[1]+0.2, pos2[1]+0.2], 'k-')
                        ax.plot([pos1[0], pos2[0]], [pos1[1]-0.2, pos2[1]-0.2], 'k-')
                    elif dy != 0:  # vertical
                        ax.plot([pos1[0]+0.2, pos2[0]+0.2], [pos1[1], pos2[1]], 'k-')
                        ax.plot([pos1[0]-0.2, pos2[0]-0.2], [pos1[1], pos2[1]], 'k-')
                # Add triple bond handling if needed

    # Draw lone pairs
    for atom, data in atoms.items():
        pos = positions[atom]
        for connection in data['connections']:
            if len(connection) == 2:  # lone pair
                direction, _ = connection
                if direction == 'right':
                    lp1 = (pos[0]+0.2, pos[1])
                    lp2 = (pos[0]+0.4, pos[1])
                elif direction == 'left':
                    lp1 = (pos[0]-0.2, pos[1])
                    lp2 = (pos[0]-0.4, pos[1])
                elif direction == 'above':
                    lp1 = (pos[0], pos[1]+0.2)
                    lp2 = (pos[0], pos[1]+0.4)
                elif direction == 'below':
                    lp1 = (pos[0], pos[1]-0.2)
                    lp2 = (pos[0], pos[1]-0.4)
                ax.plot([lp1[0]], [lp1[1]], 'ko', markersize=3)
                ax.plot([lp2[0]], [lp2[1]], 'ko', markersize=3)

    # Adjust plot limits
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]
    ax.set_xlim(min(all_x)-1, max(all_x)+1)
    ax.set_ylim(min(all_y)-1, max(all_y)+1)
    ax.axis('off')  # Hide axes for a cleaner look
    plt.title("Diethylamine Lewis Structure")
    plt.show()

# Diethylamine input
input_str = ("N1[left:-:C1, right:-:C2, below:-:H1, above::];"
             "C1[right:-:N1, left:-:C3, above:-:H2, below:-:H3];"
             "C2[left:-:N1, right:-:C4, above:-:H7, below:-:H8];"
             "C3[right:-:C1, left:-:H4, above:-:H5, below:-:H6];"
             "C4[left:-:C2, right:-:H9, above:-:H10, below:-:H11];"
             "H1[above:-:N1];H2[below:-:C1];H3[above:-:C1];H4[right:-:C3];"
             "H5[below:-:C3];H6[above:-:C3];H7[below:-:C2];H8[above:-:C2];"
             "H9[left:-:C4];H10[below:-:C4];H11[above:-:C4]")

# Run the interpreter
atoms = parse_molecule(input_str)
positions = place_atoms(atoms)
draw_molecule(atoms, positions)

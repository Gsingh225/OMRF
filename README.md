# Organic Molecule Representation Format

## Overview
This text-based format is designed to represent organic molecules comprehensively, including:
- **Lone pairs**
- **All hydrogen atoms** (no omissions)
- **Bond types** (single, double, triple)
- **Precise atom placements**
- **Formal charges**

The format is easy to read and write, allowing optional details to be omitted when desired while maintaining clarity and flexibility.

## Format Specification
Each molecule is represented as a list of **atom specifications**, where each atom is described with its connections, lone pairs, and optional formal charge.

### Atom Specification Syntax:
```
Atom_label{charge}[connection1, connection2, ...]
```
- **Atom_label**: Element symbol (e.g., `N`, `C`, `H`), optionally followed by a numerical label (e.g., `N1`, `C2`) to distinguish identical elements.
- **{charge}**: Optional formal charge, written as `{+1}`, `{-1}`, etc. If no charge exists, this part is omitted.
- **[connection1, connection2, ...]**: A comma-separated list of connections enclosed in square brackets.
  - **Bond connections**: `direction:bond_type:connected_atom`
    - `direction`: Placement relative to the atom (`left`, `right`, `above`, `below`).
    - `bond_type`: Specifies the bond (`-` for single, `=` for double, `≡` for triple).
    - `connected_atom`: The label of the atom it connects to.
  - **Lone pairs**: `direction::`
    - `direction`: Placement of the lone pair (`above::`, `below::`, etc.).
    - `::` signifies a lone pair with no connected atom.

### Rules:
- Every atom, including all hydrogens, must be explicitly listed with its connections.
- Directions (`left`, `right`, `above`, `below`) define **2D placement** relative to the atom.
- The list can be written in **single-line format** (separated by spaces or semicolons) or in **multi-line format** for readability.

## Example: Diethylamine (CH₃CH₂)₂NH
Diethylamine consists of a nitrogen atom bonded to two ethyl groups (CH₃CH₂–) and one hydrogen, with a lone pair on nitrogen.

### Atom Labeling:
- **N1**: Central nitrogen
- **C1, C3**: Left ethyl group (C1: CH₂, C3: CH₃)
- **C2, C4**: Right ethyl group (C2: CH₂, C4: CH₃)
- **H1**: Hydrogen on N1
- **H2–H11**: Hydrogens on carbons

### Representation:
```
N1[left:-:C1, right:-:C2, below:-:H1, above::]
C1[right:-:N1, left:-:C3, above:-:H2, below:-:H3]
C2[left:-:N1, right:-:C4, above:-:H7, below:-:H8]
C3[right:-:C1, left:-:H4, above:-:H5, below:-:H6]
C4[left:-:C2, right:-:H9, above:-:H10, below:-:H11]
H1[above:-:N1]
H2[below:-:C1]
H3[above:-:C1]
H4[right:-:C3]
H5[below:-:C3]
H6[above:-:C3]
H7[below:-:C2]
H8[above:-:C2]
H9[left:-:C4]
H10[below:-:C4]
H11[above:-:C4]
```

## Features
### **1. Lone Pairs**
Lone pairs are represented as `direction::`. For example, ammonia (NH₃):
```
N1[left:-:H1, right:-:H2, above:-:H3, below::]
H1[right:-:N1]
H2[left:-:N1]
H3[below:-:N1]
```

### **2. Full Representation (No Skeleton Forms)**
All atoms, including every hydrogen, are explicitly listed to provide a **complete** representation.

### **3. Human Readability**
Uses:
- Standard **chemical symbols**
- Intuitive **directions** (`left`, `right`, `above`, `below`)
- Standard **bond notation** (`-`, `=`, `≡`)

### **4. Bond Types**
Single (`-`), double (`=`), and triple (`≡`) bonds are explicitly noted. Example: Ethene (H₂C=CH₂):
```
C1[left:-:H1, right:-:H2, above:=:C2]
C2[below:=:C1, left:-:H3, right:-:H4]
H1[right:-:C1]
H2[left:-:C1]
H3[right:-:C2]
H4[left:-:C2]
```

### **5. Precise Placement**
Directions (`left`, `right`, `above`, `below`) define **2D positioning**. Example: NH₄⁺:
```
N1{+1}[left:-:H1, right:-:H2, above:-:H3, below:-:H4]
H1[right:-:N1]
H2[left:-:N1]
H3[below:-:N1]
H4[above:-:N1]
```

### **6. Formal Charges**
Charges are included in `{}`. Example: Nitronium ion (NO₂⁺):
```
N1{+1}[left:=:O1, right:=:O2]
O1[right:=:N1]
O2[left:=:N1]
```

### **7. Flexible Detail Levels**
- You can omit hydrogens, lone pairs, or charges when unnecessary.
- Example: Minimal diethylamine backbone:
```
N1[left:-:C1, right:-:C2]
C1[right:-:N1, left:-:C3]
C2[left:-:N1, right:-:C4]
C3[right:-:C1]
C4[left:-:C2]
```

## Summary
This format provides a **structured, readable, and flexible** way to represent organic molecules textually. It ensures **clarity**, **completeness**, and **ease of use** while capturing key molecular details like **lone pairs, bond types, atom placements, and charges**.

## License
This project is licensed under the MIT License.

## Contributions
Contributions, suggestions, and improvements are welcome! Feel free to submit a pull request or open an issue.

## Contact
For questions or discussions, please reach out via the GitHub Issues section.


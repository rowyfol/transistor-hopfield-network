"""
3-Node Hopfield Network Simulation
==================================
This script simulates the discrete Hopfield associative memory
that is implemented in hardware using 2N3904 transistors.

The weight matrix is derived from the stored pattern [1, 0, 1].
The simulation shows:
  1. The energy landscape (all 8 possible states)
  2. Convergence trajectories from partial/corrupted inputs

Usage:
    python hopfield_simulation.py

Output:
    hopfield_simulation.png
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 1. DEFINE THE HOPFIELD NETWORK
# ------------------------------------------------------------------

# Stored pattern in binary: [1, 0, 1]
# Convert to bipolar: 0 -> -1, 1 -> +1
pattern = np.array([1, -1, 1])

# Weight matrix: W_ij = (2*p_i - 1)(2*p_j - 1) for i != j
# No self-connections (diagonal = 0)
W = np.outer(pattern, pattern) - np.eye(3)

print("Weight Matrix W:")
print(W)
print("\nStored pattern (bipolar):", pattern)
print("Stored pattern (binary): ", (pattern + 1) // 2)

# ------------------------------------------------------------------
# 2. ENERGY & UPDATE FUNCTIONS
# ------------------------------------------------------------------

def energy(state):
    """Hopfield energy: E = -0.5 * s^T * W * s"""
    return -0.5 * np.dot(state, np.dot(W, state))

def update_sync(state):
    """Synchronous update: all neurons update at once."""
    h = np.dot(W, state)
    return np.where(h >= 0, 1, -1)

# ------------------------------------------------------------------
# 3. SIMULATE ALL 8 STATES & THEIR ENERGIES
# ------------------------------------------------------------------

states = np.array([
    [-1, -1, -1],  # [0,0,0]
    [-1, -1,  1],  # [0,0,1]
    [-1,  1, -1],  # [0,1,0]
    [-1,  1,  1],  # [0,1,1]
    [ 1, -1, -1],  # [1,0,0]
    [ 1, -1,  1],  # [1,0,1]  <-- STORED PATTERN
    [ 1,  1, -1],  # [1,1,0]
    [ 1,  1,  1],  # [1,1,1]
])

energies = [energy(s) for s in states]
labels = ['[0,0,0]', '[0,0,1]', '[0,1,0]', '[0,1,1]',
          '[1,0,0]', '[1,0,1]', '[1,1,0]', '[1,1,1]']

# ------------------------------------------------------------------
# 4. PLOT 1: ENERGY LANDSCAPE
# ------------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

colors = ['red' if l == '[1,0,1]' else 'blue' if l == '[0,1,0]' else 'gray'
          for l in labels]

ax1 = axes[0]
bars = ax1.bar(range(8), energies, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_xticks(range(8))
ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)
ax1.set_ylabel('Energy E = -½ sᵀWs', fontsize=12)
ax1.set_title('Energy Landscape of 3-Node Hopfield Network', fontsize=13, fontweight='bold')
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.grid(axis='y', alpha=0.3)

for i, (e, l) in enumerate(zip(energies, labels)):
    if l == '[1,0,1]':
        ax1.annotate('STORED\nMEMORY', xy=(i, e), xytext=(i, e + 0.5),
                    ha='center', fontsize=9, fontweight='bold', color='darkred',
                    arrowprops=dict(arrowstyle='->', color='darkred'))
    elif l == '[0,1,0]':
        ax1.annotate('INVERSE\nSPURIOUS', xy=(i, e), xytext=(i, e + 0.5),
                    ha='center', fontsize=9, fontweight='bold', color='darkblue',
                    arrowprops=dict(arrowstyle='->', color='darkblue'))

# ------------------------------------------------------------------
# 5. PLOT 2: CONVERGENCE TRAJECTORIES
# ------------------------------------------------------------------

ax2 = axes[1]

initial_states = [
    np.array([1, -1, -1]),   # [1,0,0] - partial cue (only N1)
    np.array([-1, -1, 1]),   # [0,0,1] - partial cue (only N3)
    np.array([1, 1, -1]),    # [1,1,0] - corrupted (N2 should be off)
    np.array([-1, 1, -1]),   # [0,1,0] - inverse pattern
]

trajectory_labels = [
    'Start: [1,0,0] (only N1)',
    'Start: [0,0,1] (only N3)',
    'Start: [1,1,0] (N2 corrupted)',
    'Start: [0,1,0] (inverse)',
]

colors_traj = ['green', 'orange', 'purple', 'brown']

for s0, label, color in zip(initial_states, trajectory_labels, colors_traj):
    states_hist = [s0.copy()]
    s = s0.copy()
    for _ in range(10):
        s_new = update_sync(s)
        states_hist.append(s_new.copy())
        if np.array_equal(s, s_new):
            break
        s = s_new

    # Convert bipolar [-1,1] to binary [0,1] for plotting
    binary_hist = [(s + 1) // 2 for s in states_hist]
    # Encode state as decimal: 4*N1 + 2*N2 + 1*N3
    y_vals = [np.dot(b, [4, 2, 1]) for b in binary_hist]
    x_vals = list(range(len(binary_hist)))

    ax2.step(x_vals, y_vals, where='post', color=color, linewidth=2.5,
             label=label, marker='o')

ax2.set_xlabel('Update Step', fontsize=12)
ax2.set_ylabel('State (decimal: 4*N1 + 2*N2 + 1*N3)', fontsize=12)
ax2.set_title('Network Convergence from Partial / Corrupted Inputs',
              fontsize=13, fontweight='bold')
ax2.set_xticks(range(6))
ax2.set_yticks(range(8))
ax2.set_yticklabels(['[0,0,0]', '[0,0,1]', '[0,1,0]', '[0,1,1]',
                     '[1,0,0]', '[1,0,1]', '[1,1,0]', '[1,1,1]'])
ax2.axhline(y=5, color='red', linestyle='--', linewidth=1.5, alpha=0.7,
            label='Target [1,0,1]')
ax2.legend(loc='center right', fontsize=9)
ax2.grid(alpha=0.3)
ax2.set_xlim(-0.5, 5.5)

plt.tight_layout()
plt.savefig('hopfield_simulation.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.show()

print("\nSimulation complete! Saved: hopfield_simulation.png")
print("\nKey findings:")
print(f"- Energy of [1,0,1] (stored):  {energy(np.array([1, -1, 1])):.1f}")
print(f"- Energy of [0,1,0] (spurious): {energy(np.array([-1, 1, -1])):.1f}")
print("- Partial inputs [1,0,0] and [0,0,1] both converge to [1,0,1]")

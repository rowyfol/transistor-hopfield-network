# 3-Node Transistor Hopfield Network
**Discrete Bistable Associative Memory — Built with Only Transistors, Resistors, Diodes & LEDs**

> A hardware implementation of a 3-node Hopfield-style associative memory using discrete BJT transistors (2N3904). No ICs, no logic gates, no op-amps. Designed for a university Electronics I course.

---

## 📋 Abstract

This project demonstrates how **associative memory** — the ability to recall a complete pattern from a partial cue — can be implemented in hardware using only basic analog components. 

Each memory "node" is a **bistable multivibrator (Eccles-Jordan flip-flop)** built from two NPN transistors. Three such nodes are cross-coupled via an **inter-nodal weight network** (potentiometers and diodes) to form a discrete Hopfield network. The network is trained (hard-wired) to store the pattern **[1, 0, 1]**, meaning Nodes 1 and 3 are mutually excitatory while Node 2 is mutually inhibitory with both.

When a partial pattern is presented (e.g., only Node 1 is activated), the network converges to the stored stable state **[1, 0, 1]** through transistor-level feedback.

---

## 🧠 Theory

### What is Associative Memory?
Unlike conventional addressable memory (RAM), associative memory retrieves data by **content**, not by address. In neural networks, this is modeled by the **Hopfield Network** (1982), where a fully-connected network of neurons converges to a stored energy minimum (memory state) from a noisy or partial input.

### Why Bistable Multivibrators?
A single transistor is merely a switch — it forgets its state when the input is removed. To create "memory," each node must be **bistable**: it has two stable equilibrium states and remains in whichever state it was last forced into.

The **Eccles-Jordan flip-flop** (two cross-coupled NPN transistors) provides exactly this. Positive feedback between the two transistors creates a latch that holds its state indefinitely without continuous input.

---

## ⚡ Circuit Architecture

### Node Structure (×3)
Each node consists of:
- **Two 2N3904 NPN transistors** (Q_iA, Q_iB) forming a bistable pair
- **Cross-coupling resistors** (100kΩ) between collectors and opposite bases
- **Base pull-down resistors** (100kΩ) to prevent noise-triggering
- **Collector load resistors** (1kΩ) to Vcc
- **LED + 330Ω series resistor** on Q_iA to indicate the active state
- **SET button** (momentary) to force the node into the ON state
- **RESET diode** to allow global clearing

**State Table per Node:**

| State | Q_iA | Q_iB | LED | Q_iB Collector |
|-------|------|------|-----|----------------|
| **ON** | ON | OFF | 🔴/🟡/🟢 | **HIGH (~6V)** |
| **OFF** | OFF | ON | OFF | LOW (~0V) |

> The **Q_iB collector** acts as the node's "status output." It is HIGH when the node is active, making it the perfect source for inter-nodal coupling.

### Inter-Nodal Coupling (The Synaptic Weights)
The network stores the pattern **[1, 0, 1]** via two types of coupling:

| Type | Connection | Component | Effect |
|------|-----------|-----------|--------|
| **Excitatory** | N1 ↔ N3 | 1N4148 + 100kΩ Pot | "Friend" — turns the other node ON |
| **Inhibitory** | N1→N2, N2→N1, N2→N3, N3→N2 | 10kΩ Pot | "Enemy" — turns the other node OFF |

- **Excitatory links** use a **diode** to ensure one-way current flow. When the source node is active, its Q_iB collector is HIGH, sending current through the diode to the target node's **Q_jA base**, turning it ON.
- **Inhibitory links** connect to the target node's **Q_jB base**. Turning Q_jB ON forces Q_jA OFF, suppressing the target node.

### Global Control
- **SET1 / SET2 / SET3**: Momentary buttons that inject Vcc into the respective Q_iA base, forcing that node into the ON state.
- **RESET**: A momentary button that pulls all Q_iA bases to GND via isolation diodes, forcing every node into the OFF state.

---

## 🛠️ Hardware Implementation

### Power Supply
- **6V** from 4× AA batteries (no voltage regulator module needed).

### Component List
| Component | Value | Quantity | Role |
|-----------|-------|----------|------|
| Transistor | 2N3904 (NPN) | 6 | 3 bistable flip-flops |
| Resistor | 1kΩ | 15 | Collector loads, SET protection |
| Resistor | 100kΩ | 12 | Cross-coupling, pull-downs |
| Resistor | 330Ω | 3 | LED current limiting |
| Resistor | 220Ω | 3 | LED current limiting (optional series) |
| Potentiometer | 100kΩ | 2 | Excitatory weight tuning |
| Potentiometer | 10kΩ | 4 | Inhibitory weight tuning |
| Diode | 1N4148 | 2 | Excitatory path isolation |
| LED | 5mm Red / Yellow / Green | 1 each | State indicators |
| Push Button | 6×6mm Tactile | 4 | SET ×3 + RESET |
| Breadboard | MB-102 | 1 | Prototyping |
| Jumper Wires | Male-to-Male | 1 set | Connections |

### Schematic
> See [`/schematics/`](./schematics/) for the full KiCad schematic and PDF.

### Breadboard Layout
> See [`/docs/breadboard_layout.png`](./docs/) for the step-by-step wiring guide.

---

## 🎬 Operation & Demo

### Stored Pattern: [1, 0, 1]
- Node 1 (Red) = **ON**
- Node 2 (Yellow) = **OFF**
- Node 3 (Green) = **ON**

### Test Cases

| Action | Initial State | Result | Explanation |
|--------|--------------|--------|-------------|
| **Press RESET** | Any | [0, 0, 0] | All nodes cleared |
| **Press SET1** | [0, 0, 0] | [1, 0, 1] | N1 turns ON → excites N3 via D13; N1 & N3 inhibit N2 |
| **Press SET3** | [0, 0, 0] | [1, 0, 1] | N3 turns ON → excites N1 via D31; N1 & N3 inhibit N2 |
| **Press SET1 + SET2** | [0, 0, 0] | [1, 0, 1] | N1 & N2 both triggered, but N2 is suppressed by N1/N3 feedback |
| **Press SET2 alone** | [0, 0, 0] | [0, 1, 0] | N2 has no excitatory friends; it suppresses N1 & N3 but they have no reason to turn on. The network settles to the inverse pattern [0, 1, 0]. |

### Convergence Behavior
This is the core "associative" property:
1. Present a **partial cue** (e.g., only Node 1).
2. The internal coupling network processes the signal through transistor feedback.
3. The system **settles** into the nearest stable energy minimum: the stored memory **[1, 0, 1]**.

---

## 📁 Repository Structure
├── README.md ├── schematics/ │ ├── transistor-associative-memory.kicad_sch │ └── schematic.pdf ├── docs/ │ ├── theory_hopfield_network.md │ ├── breadboard_layout.png │ └── component_datasheets/ ├── photos/ │ ├── breadboard_front.jpg │ ├── breadboard_closeup.jpg │ └── demo_video.mp4 └── reports/  └── electronics1_project_report.pdf


---

## 🎓 Project Context

- **Course:** Electronics I (Analog & Discrete Circuit Design)
- **Constraint:** No integrated circuits (ICs), logic gates, or op-amps allowed
- **Objective:** Demonstrate feedback, bistability, latching, and neural-network concepts using only discrete components
- **Inspiration:** John Hopfield's 1982 paper on neural networks and early 1960s hardware neuron models

---

## 🔬 Key Concepts Demonstrated

1. **Bistable Multivibrator** — Positive feedback, two stable states, memory/latching
2. **Cross-Coupled Transistor Pair** — Eccles-Jordan flip-flop
3. **Analog Neural Network** — Discrete implementation of synaptic weights
4. **Associative Recall** — Pattern completion from partial input
5. **Diode Isolation** — One-way coupling and reset protection
6. **Potentiometer Tuning** — Analog weight adjustment (synaptic plasticity)

---

## 📚 References

1. Hopfield, J. J. (1982). "Neural networks and physical systems with emergent collective computational abilities." *PNAS*.
2. Millman & Halkias, *Integrated Electronics: Analog and Digital Circuits and Systems* — Chapter on Bistable Multivibrators.
3. Boylestad & Nashelsky, *Electronic Devices and Circuit Theory* — Flip-Flops and Feedback Amplifiers.

---

## 📝 License

This project is released for academic and educational purposes. Feel free to fork and build your own discrete neural network!

---

**Built with 🔧, ⚡, and a lot of 2N3904s.**

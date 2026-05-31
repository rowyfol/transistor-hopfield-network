# Transistor Associative Memory (ELEC I Project)

A fully discrete hardware implementation of a pattern recognition / associative memory system using only bipolar junction transistors (BJTs), resistors, LEDs, and passive components — no microcontrollers or integrated circuits.

## Overview

This project demonstrates how simple transistor-level circuits can perform basic pattern classification and associative behavior, inspired by early neural network and threshold logic models.

Instead of software or digital ICs, all logic is implemented using current summation through resistor networks and transistor switching thresholds.

The system responds to specific input combinations by activating corresponding outputs, effectively acting as a small hardware pattern classifier.

## Concept

The circuit maps input combinations to outputs:

- A + B → Green LED  
- B + C → Yellow LED  
- A + C → Red LED  

Each output behaves like a threshold decision unit, where combined input currents determine whether a transistor switches ON or OFF.

## Key Idea

Weighted input currents + transistor threshold = decision output

This project is a hardware implementation of a simplified perceptron-like classifier using discrete electronics.

## Features

- Fully discrete transistor logic (no ICs)
- Pattern recognition via input combinations
- Hardware-based threshold decision making
- Real-time physical demonstration
- Expandable architecture for more inputs or outputs

## Components Used

### Active Components
- 3× 2N3904 NPN transistors
- 3× LEDs (Red, Yellow, Green)

### Passive Components
- 6× 100kΩ resistors (input weighting network)
- 3× 330Ω resistors (LED current limiting)
- 3× 1kΩ resistors (base protection / tuning)
- 3× push buttons (inputs A, B, C)

### Power Supply
- 4× AA battery pack (~6V)

### Other
- Breadboard
- Jumper wires

## How It Works

Each input button applies voltage through a resistor network. When multiple inputs are active, their currents combine at the base of a transistor.

If the combined current exceeds the transistor’s switching threshold, the transistor turns ON and activates the corresponding LED.

Different resistor values act as “weights,” controlling how strongly each input contributes to the decision.

## System Architecture

Inputs (A, B, C)
→ Weighted resistor network
→ Transistor decision nodes (NPN BJTs)
→ Output LEDs (classification results)

## Example Behavior

- A + B → Green LED ON  
- B + C → Yellow LED ON  
- A + C → Red LED ON  

Single inputs should not activate outputs; only valid combinations exceed the switching threshold.

## Educational Purpose

This project demonstrates:

- Transistor switching behavior (cutoff and saturation regions)
- Analog summation of currents
- Threshold-based decision making
- Hardware implementation of classification logic
- Foundational concepts behind neural computation

## Possible Extensions

- Increase number of inputs for higher-dimensional classification
- Add memory using transistor latch circuits
- Introduce capacitors for temporal behavior (short-term memory effects)
- Build multi-layer transistor networks for more complex logic

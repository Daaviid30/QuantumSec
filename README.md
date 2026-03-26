# QKD-PQC Simulation Framework

A modular simulation framework for analyzing the impact of post-quantum authentication mechanisms on Quantum Key Distribution (QKD) protocols.

## 📌 Overview

This project aims to bridge the gap between theoretical quantum cryptography and practical secure system design by focusing on a critical but often overlooked component:

> **The authentication of the classical channel in QKD systems under post-quantum threat models.**

While QKD provides information-theoretic security for key exchange, it relies on classical authentication mechanisms that are vulnerable to quantum attacks (e.g., Shor’s algorithm). This framework enables the evaluation of such mechanisms in realistic protocol scenarios.

---

## 🎯 Objectives

- Model QKD protocols (BB84, B92, E91) at a logical and operational level.
- Simulate the classical communication channel and its exposure to attacks (e.g., Man-in-the-Middle).
- Integrate and compare different authentication schemes:
  - Classical (MAC, ECDSA)
  - Post-Quantum (e.g., CRYSTALS-Dilithium)
  - Hybrid approaches
- Evaluate the impact of authentication on:
  - Communication overhead
  - Latency
  - Key generation rate
  - Scalability

## 🏗️ Architecture

The framework is designed as a modular and extensible system:
QuantumSec/
├── qkd/ # QKD protocols (BB84, E91, B92)
├── auth/ # Authentication schemes (classical, PQC, hybrid)
├── math/ # Mathematical abstractions (bits, bases, measurements)
├── network/ # (Future investigation) QKD network simulation
├── experiments/ # Experimental scenarios and evaluations
├── configs/ # Configuration files
└── main.py # Entry point


### Core Components

- **QKD Module**  
  Logical implementation of QKD protocols with clear phase separation.

- **Authentication Module**  
  Pluggable authentication schemes for securing the classical channel.

- **Mathematical Layer**  
  Lightweight abstractions for modeling quantum-like behavior.

- **Experiment Engine**  
  Enables reproducible evaluation and comparison across different configurations.

---

## 🔐 Research Focus

The main research question addressed by this framework is:

> **How do post-quantum authentication mechanisms affect the security and operational performance of QKD systems?**

## 🎓 Academic Context

This project is developed as part of a Master's thesis focused on:

Post-Quantum Cryptography (PQC)
Quantum Key Distribution (QKD)
Secure system design under quantum threat models

It is designed to serve as a foundation for future research, including potential PhD work.

⚠️ Disclaimer

This framework is intended for research and educational purposes.
It does not aim to provide production-ready cryptographic implementations.

👤 Author

David Martín Castro

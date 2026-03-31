# 3-SAT Optimization via Simulated Annealing

## Overview
This project studies the 3-SAT problem as a Constraint Satisfaction Problem (CSP) and investigates its solvability using Simulated Annealing.

## Key Contributions
- Efficient vectorized cost function
- Delta-cost optimization using clause tracking
- Empirical analysis of phase transition in satisfiability

## Results

* Identification of an empirical algorithmic threshold at **M/N ≈ 4.05**, close to the theoretical value (~4.25)
* Clear **phase transition behavior**: solvability drops sharply as constraint density increases
* High solvability (P ≈ 1) for low M/N, followed by a rapid transition to unsatisfiable regimes
* Performance degradation due to increasingly complex energy landscape with many local minima

## Structure
- `src/` → core implementation
- `report.pdf` → theoretical analysis and results

## Tech Stack
Python · NumPy · Optimization · Simulated Annealing

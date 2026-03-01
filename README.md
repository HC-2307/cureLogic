# CureLogic

## Overview

CureLogic is a physics informed AI based concrete curing optimization platform.  
It combines maturity modeling principles with machine learning prediction to estimate compressive strength development, optimize steam curing duration, and reduce energy consumption while meeting required strength targets.

The system integrates material mix parameters and curing regime variables to simulate strength gain over time and recommend optimal curing strategies.

---

## Core Functionalities

### 1. Mix Design Input Control

The system allows structured control of key mix design parameters:

- Water Cement Ratio
- SCM Content Percentage
- Admixture Percentage

These parameters directly influence strength development and maturity evolution.

---

### 2. Curing Regime Configuration

Users can configure curing conditions including:

- Ambient Temperature
- Steam Temperature
- Steam Duration
- Required Target Strength

These inputs are used to simulate strength gain curves and evaluate curing effectiveness.

---

### 3. Physics Based Maturity Modeling

The platform incorporates maturity modeling concepts to compute strength gain as a function of:

- Temperature history
- Time progression
- Maturity index accumulation

This ensures predictions are grounded in physical curing behavior rather than purely statistical fitting.

---

### 4. Machine Learning Strength Prediction

A trained Gradient Boosting Regressor predicts compressive strength using:

- Water Cement Ratio
- SCM Percentage
- Steam Duration
- Steam Temperature
- Ambient Temperature
- Maturity Index
- Admixture Percentage

The model is trained on synthetic curing cycle data to simulate realistic strength development patterns.

---

### 5. Strength Gain Curve Visualization

The application generates:

- Predicted strength curve
- Physics based maturity curve
- Target strength reference line
- Steam end marker

This allows comparison between predicted performance and required design strength.

---

### 6. Optimal Steam Duration Estimation

The system determines:

- Minimum steam duration required to reach target strength
- Current curing status
- Strength deficit if target is not met

This enables cycle time optimization.

---

### 7. Energy Saving Estimation

Energy savings are calculated relative to a baseline curing regime.

The platform estimates:

- Reduced steam hours
- Relative energy cost comparison
- Efficiency improvement percentage

---

### 8. Hourly Strength Table

The application generates a detailed curing table including:

- Hour
- Temperature
- Maturity Index
- Physics Model Strength
- ML Predicted Strength
- Readiness Status

This provides traceable curing progression data.

---

### 9. Optimization Recommendations

The system provides actionable recommendations such as:

- Increasing or decreasing steam duration
- Adjusting water cement ratio
- Strength improvement potential
- Cycle optimization suggestions

---

## Prototype Workflow

1. User defines mix design parameters.
2. User configures curing regime.
3. Maturity index is calculated over time.
4. Physics based strength curve is computed.
5. ML model predicts compressive strength.
6. Target strength comparison is performed.
7. Optimal steam duration is determined.
8. Energy efficiency metrics are generated.
9. Recommendations are displayed.

---

## System Characteristics

- Physics informed AI architecture
- Deterministic strength evaluation
- Maturity driven modeling
- Steam curing optimization
- Energy efficiency estimation
- Structured decision output
- Expandable ML framework

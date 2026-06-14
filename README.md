<p align="center">
  <img src="images/logo.png" alt="SLIIT ROBOFEST 2026 Logo" width="200"/>
</p>

# SLIIT ROBOFEST 2026 — University Category
## Technical Specifications & Competition Guidelines

This document provides the complete technical specifications, rules, and procedures for designing, building, and competing with an autonomous Micromouse robot.

---

## 1. Introduction & Challenge Concept

### 🎯 Theme: "DESIGN. DEPLOY. DOMINATE."
The **Micromouse Challenge** is a test of autonomy, intelligence, and speed. Competitors must engineer a self-contained, fully autonomous robot capable of exploring, mapping, and navigating through a physical maze to find the fastest path from the starting cell to the central destination goal.

> [!NOTE]
> The maze's physical structure remains fixed for a given round, but its complexity tests the robot's real-time decision-making, adaptive algorithms, and precise control systems. The fastest and most efficient Micromouse wins the challenge.

---

## 2. Micromouse Robot Specifications

All competing robots must undergo and pass an initial inspection. The key hardware constraints are summarized below:

<table border="1" style="border: 1px solid black; border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="background-color: #290877ff;">
      <th style="border: 1px solid black; padding: 8px; text-align: left; width: 25%;">Constraint Category</th>
      <th style="border: 1px solid black; padding: 8px; text-align: left;">Requirement Specification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Dimensions</strong></td>
      <td style="border: 1px solid black; padding: 8px;">Maximum length of <strong>14.5 cm</strong> and maximum width of <strong>14.5 cm</strong>. No height restrictions.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Weight</strong></td>
      <td style="border: 1px solid black; padding: 8px;">Must remain constant. Any replacement batteries must keep overall weight within <strong>&plusmn; 5g</strong> of the initial inspection weight. Re-weighed if other components are replaced.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Voltage Limit</strong></td>
      <td style="border: 1px solid black; padding: 8px;">The voltage between any two points in the circuitry must not exceed <strong>24V</strong> at any given time.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Power Source</strong></td>
      <td style="border: 1px solid black; padding: 8px;">No combustion processes or pollutant-emitting power sources are permitted.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Wireless Communication</strong></td>
      <td style="border: 1px solid black; padding: 8px;">RF modules (Bluetooth, Wi-Fi, NRF, etc.) must be disabled or powered off during the competition. No external telemetry is allowed.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Dislodged Parts</strong></td>
      <td style="border: 1px solid black; padding: 8px;">The robot must not leave any part of its body behind while navigating.</td>
    </tr>
  </tbody>
</table>

### 🧭 Autonomy & Safety
* **Self-Containment:** The Micromouse must be completely self-contained and receive no outside assistance, remote signals, or code updates after initial inspection.
* **Operation Modes:** Manual physical switches on the robot are permitted to select pre-programmed operating modes/algorithms prior to starting a run.
* **Locomotion Restrictions:** The robot is not allowed to jump over, fly over, climb, scratch, cut, burn, mark, damage, or destroy the walls of the maze.

---

## 3. Maze Specifications & Geometry

### 📐 Dimensions and Layout

<table border="1" style="border: 1px solid black; border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="background-color: #290877ff;">
      <th style="border: 1px solid black; padding: 8px; text-align: left; width: 25%;">Parameter</th>
      <th style="border: 1px solid black; padding: 8px; text-align: left;">Dimension</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Grid Layout</strong></td>
      <td style="border: 1px solid black; padding: 8px;">16 &times; 16 unit cells.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Unit Cell</strong></td>
      <td style="border: 1px solid black; padding: 8px;">18 cm &times; 18 cm.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Total Pitch</strong></td>
      <td style="border: 1px solid black; padding: 8px;">Length from a wall to the far edge of a lattice point is 19.2 cm.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Maze Walls</strong></td>
      <td style="border: 1px solid black; padding: 8px;">5 cm high and 1.2 cm thick (with &plusmn; 5% construction tolerance).</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Lattice Points (Posts)</strong></td>
      <td style="border: 1px solid black; padding: 8px;">1.2 cm &times; 1.2 cm wide and 5 cm high. Located at the four corners of each cell. At least one wall connects to each post (except destination square).</td>
    </tr>
  </tbody>
</table>

<br/>

![Figure 2: Maze Dimensions (units in mm)](images/figure%202.png)

### 🧱 Materials and Aesthetics
* **Construction:** Made of high-quality PVC sheets.
* **Floor Finish:** Covered with a non-gloss black sticker.
* **Wall Finish:** Coated in non-gloss white, with the top edge colored red.

> [!WARNING]
> Minor variations in wall color, floor seams, and ambient light levels may exist. Robot sensor designs must be robust enough to handle varying ambient lighting, fluorescent lights, or sunlight at the venue.

### 🚩 Start and Destination Goal
* **Starting Cell:** Located at one of the four corners of the maze, bound by walls on three sides. The **Start Line** is the boundary between the first and second cell.
* **Destination Goal:** A $2 \times 2$ cell square (4 cells total) near the center of the maze. It has only **one entrance**. The **Finish Line** is the entry line leading into the destination cell.
  * *Note: Multiple paths to the destination may exist.*

![Figure 1: Sample Maze Layout](images/figure%201.png)

---

## 4. Run Allocations & Penalties

Rules for time slots, runs, and penalties are structured as follows:

<table border="1" style="border: 1px solid black; border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="background-color: #290877ff;">
      <th style="border: 1px solid black; padding: 8px; text-align: left; width: 25%;">Item</th>
      <th style="border: 1px solid black; padding: 8px; text-align: left; width: 37.5%;">Elimination Round</th>
      <th style="border: 1px solid black; padding: 8px; text-align: left; width: 37.5%;">Final Round</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Time Allocation</strong></td>
      <td style="border: 1px solid black; padding: 8px;"><strong>8 minutes</strong> Trial Time (timer starts when granted permission, includes adjustment/setup time).</td>
      <td style="border: 1px solid black; padding: 8px;"><strong>12 minutes</strong> Competition Time (any setup/adjustment between runs is included in a 10-minute slot).</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Max Attempts (Runs)</strong></td>
      <td style="border: 1px solid black; padding: 8px;">5 runs.</td>
      <td style="border: 1px solid black; padding: 8px;">10 runs.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Contact Penalty</strong></td>
      <td style="border: 1px solid black; padding: 8px;" colspan="2"><strong>+3 seconds</strong> added to Run Time per wall collision. Successive collisions within 3 seconds count as a single penalty.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Reset Penalty</strong></td>
      <td style="border: 1px solid black; padding: 8px;" colspan="2"><strong>+20 seconds</strong> added to Run Time if the robot is manually reset from the destination cell back to the starting cell (instead of navigating back autonomously).</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Stuck Robot (Restart)</strong></td>
      <td style="border: 1px solid black; padding: 8px;" colspan="2">With judge permission, a stuck robot can be lifted and placed back in the starting cell. This terminates the current run; no Run Time is recorded.</td>
    </tr>
    <tr>
      <td style="border: 1px solid black; padding: 8px;"><strong>Qualifying / Official Time</strong></td>
      <td style="border: 1px solid black; padding: 8px;">Shortest recorded Run Time (with penalties) is used to rank and filter teams for finals.</td>
      <td style="border: 1px solid black; padding: 8px;">Shortest recorded Run Time (with penalties) determines final placing.</td>
    </tr>
  </tbody>
</table>

### 🛠️ Adjustments & Repairs
* **Permitted Adjustments (Only in the Start Cell, before a run):** Change manual switch/speed settings, replace batteries (keeping weight within limit), adjust sensors, or make repairs with judge approval.
* **Repairs & Replacements:** Replacements must match original component specifications and weight. Microcontroller or memory replacements in the final round require approval, and the robot must run the original pre-inspected code without modification or pre-loaded maze data.
* **No-Run Score:** If a robot fails to complete a run, a ranking score is calculated based on proximity to the destination and cells explored.

---

*SLIIT ROBOFEST 2026 — Faculty of Engineering, Sri Lanka Institute of Information Technology.*

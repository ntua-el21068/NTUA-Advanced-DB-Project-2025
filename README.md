# NTUA-Advanced-DB-Project-2025
# Advanced Topics in Database Systems (2025-2026) - NTUA
**Semester Project**

**Team 41:**
* Γρηγόρης Χαμαράκης (03121068)
* Βικτωρία Κορακοβούνη (03119922)

## Description
This repository contains the implementation for the semester project using Apache Spark (PySpark).

## Contents
* `project_setup.py`: Initialization of Spark Session, Sedona Context, and configuration of data paths.
* `Query1.ipynb`: Analysis for victim age groups.
* `Query2.ipynb`: Analysis for victim descent statistics.
* `Query3.ipynb`: Analysis for Modus Operandi (MO) codes.
* `Query4.ipynb`: Geospatial analysis for Police Stations (Sedona).
* `Query5.ipynb`: Spatial join and correlation analysis (Income vs Crime Rate).

## How to Run
1. Open the notebooks in a Jupyter Environment capable of running Apache Spark >= 3.5.
2. Ensure `apache-sedona` (v1.6.1) is installed (required for Queries 4 and 5).
3. **Each notebook is self-contained.** You can open any notebook (`Query1.ipynb` - `Query5.ipynb`) and execute the cells sequentially from top to bottom.
4. Necessary library imports, Spark Session initialization, and configurations are handled within the initial cells of each notebook.
5. Adjust the S3 bucket paths in the variables `CRIME_PATH`, `CENSUS_PATH`, etc., if running in a different environment than the one provided.

## Notes
For Query 5, optimizations (Column Pruning, Geometry Simplification) were applied to handle memory constraints.

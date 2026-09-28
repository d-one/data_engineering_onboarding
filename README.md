#  D ONE Hands-On Data Engineering & Modelling Workshop

Welcome to the **D ONE Internal Data Engineering & Modelling Workshop Series**! 

This repository contains a two-part hands-on workshop designed to guide junior consultants through building an end-to-end operational data platform on **Databricks Unity Catalog**. You will move from ingesting and cleansing raw multi-format files to modeling an enterprise **Star Schema** with **Slowly Changing Dimensions (SCD Type 2)** and automating pipeline updates using **Databricks Jobs**.

---

## 📁 Repository Structure

```text
.
├── README.md                           # Workshop overview & setup instructions
├── __setup                             # Config script
├── Images/                             # Images used in the workshop
├── Notebook_1/                         # Part 1: Environment, Profiling & Medallion Pipeline
    ├──  01_medallion_pipeline
    └──  Solutions_01_medallion_pipeline
├── Notebook_2/                         # Part 2: Star Schema, SCD Type 2 & Job Verification
    ├──  02_star_schema_and_scd2
    ├──  Solutions_02_star_schema_and_scd2
    └──  job_update_maya.py        
└── Raw_files/                          # Landing files uploaded during Workshop Part 1
    ├── raw_consultants.csv             # HR Roster (CSV with duplicates & missing fields)
    ├── raw_timesheets.json             # Time Logs (JSON with negative hours & corrupt dates)
    └── raw_projects.parquet            # PMO Metadata (Parquet with project budgets)
# AI-Powered Cloud Threat Hunting Simulations

A repository of interactive Jupyter notebooks demonstrating hypothesis-driven, AI-assisted threat hunting across multi-cloud environments (AWS, Azure, GCP), aligned with the MITRE ATT&CK framework.

## Project Overview

This project bridges the gap between theoretical knowledge and practical application in cloud security. It provides a structured, hands-on learning environment where users can practice threat hunting using high-fidelity, synthetic logs that mirror real-world attack scenarios.

The simulation utilizes AI to accelerate the analysis and query generation process, reflecting modern SecOps workflows.

## Key Features

*   **AI-Assisted Workflows:** Learn how to leverage AI/ML to formulate hypotheses, generate SIEM queries, and summarize findings.
*   **MITRE ATT&CK Aligned:** Each simulation focuses on specific Tactics, Techniques, and Procedures (TTPs) used by adversaries in the wild.
*   **Multi-Cloud Focus:** Scenarios are designed to be applicable across major cloud providers (initially M365/Azure, expanding to AWS and GCP).
*   **Synthetic Data:** Safely practice using realistic JSON-formatted synthetic logs without compliance concerns or PII exposure.
*   **Comprehensive PDR:** Each module covers the full lifecycle: Prevention, Detection, and Remediation guidance.


## Available Hunting Modules

The table below indexes the available threat-hunting scenarios. Click the notebook link to view the detailed simulation, which includes the attack scenario, synthetic logs, hypotheses, and detection steps.

> **Use code with caution.**

| MITRE TTP     | Technique Name                                   | Cloud Platform Focus     | Notebook Link |
|---------------|--------------------------------------------------|---------------------------|----------------|
| T1566.001     | Spearphishing Attachment                         | M365 / Azure / GCP            | [View Notebook (T1566.001)](link_to_your_T1566_notebook_file) |
| T1078.004     | Valid Accounts: Cloud Accounts                   | AWS / Azure / GCP         | Planned        |



## Technical Stack

*   **Primary Language:** Python (Jupyter Notebooks)
*   **Data Format:** JSON (Synthetic Logs)
*   **Query Languages:** Kusto Query Language (KQL), basic SQL/Pandas , Athena queries for log analysis



## Contributions & Contact

This project is a personal initiative to share and refine cloud threat hunting methodologies.

Feel free to reach out via [Your LinkedIn Profile Link] or [Your Email Address] for collaboration or feedback.

---
**License:** [Specify your license here, e.g., MIT License]

# PASSENGER RETENTION AND ACCOUNT PORTFOLIO DIAGNOSTIC PLATFORM: 

An analytics engine and live tracking dashboard designed to transition transactional passenger datasets into a predictive dual-axis risk management matrix. This platform maps soft-churn probabilities against audited customer lifetime values (CLV) to automate margin-safe operational playbooks.

### Core Assets & Gateways: 
* **Live Web Application:** [Access Interactive Streamlit Cloud Interface] **https://airline-project.streamlit.app/** 
* **Strategic Dossier:** [Download Complete Technical Report (PDF)]

---

## Competition Context: 
This repository forms the core technical submission for the data-driven case challenge hosted by the **Consulting & Analytics Club, IIT Guwahati (C&A)**. 

The analytical objectives are built around optimizing real-world loyalty metrics to bridge the operational gap between commercial marketing scaling (CMO Priorities) and margin protection asset management (CFO Priorities).

* **Organizing Body:** Consulting & Analytics Club, IIT Guwahati
* **Project Framework:** Case Problem Matrix
* **Target Focus:** Applied Customer Data Analytics, Lifecycle Segmentation, and Financial Risk Isolation.

---

## Usage Features (What the Dashboard Does)

* **Interactive Strategy Controls Sidebar:** Allows operators to instantly slice the customer database by choosing a specific Valuation Archetype (Value Class) and a Risk Grade Profile simultaneously.
* **Dynamic Color-Coded Status Alerts:** The system changes colors automatically depending on the selected risk profile—shifting to bright Red for high-urgency rescue alerts and turning to corporate Gray or Blue for lower-priority, stable segments.
* **Live Operational Checklists:** The sidebar displays a dynamically changing interactive to-do list. Analysts get a tailored step-by-step blueprint describing exactly what operational actions to take for that specific customer cohort.
* **Real-Time KPI Data Blocks:** Displays live macro-metrics right at the top of the workspace, showing the Total Active Base, the total Imminent Risk Pipeline, and the exact count of the currently filtered customer matching group.
* **Tab-Based Workspace Architecture:** Organizes the primary screen layout into four clean, functional areas:
  * *Campaign Workspace* (For active user management)
  * *Side-by-Side Account Cross-Examination* (For individual folder auditing)
  * *Portfolio Macro Analytics* (For high-level graphs and trends)
  * *Core Criteria Documentation* (For system standard operating guidelines)

---

Architecture & Data Features (How It Works Under the Hood)

* **Smart Data-Cleaning Layer:** Missing information inside the database (like blank passenger salary entries) is resolved by matching a profile's registered Province, City, and Education Level against regional medians instead of using arbitrary averages that skew report data.
* **Isolating "Ghost Members":** Detects and segments 573 accounts that registered but never logged a single flight. Rather than treating them as broken lines or trash data, they are grouped into a standalone cohort ("Grade E") for low-cost digital marketing re-engagement.
* **Dual-Axis Query Intersection Engine:** Runs high-speed background filtering scripts through all 16,732 active row portfolios. It safely computes complex overlaps (such as isolating the 25 ultra-premium Class 1 accounts hidden inside a wider pool of 42 high-risk profiles).
* **Unified Interface Content Router:** Built using a strict, single boolean evaluation layer. This ensures that the user criteria chosen in the sidebar dynamically controls both the layout colors and the text metrics displayed on the main content page without running into sync errors.
* **Automated Data Suppression (Blackout Protocol):** Includes safety routing logic that immediately shuts off and blacklists active promotional marketing streams for profiles categorized under "Grade D - Already Cancelled" to prevent compliance violations.

---

## Cloud Deployment Architecture:

The system is deployed directly onto the **Streamlit Community Cloud** pipeline infrastructure. 
* **Data Source Layer:** Core datasets (`Customer Loyalty History.csv`, `Customer Flight Activity.csv`, etc.) are processed on-the-fly inside memory-efficient Pandas dataframes directly from the repository main branch root.
* **Execution State:** Session caching features are implemented to ensure sub-second rendering response frames during multi-tier dropdown filtering actions, eliminating lagging or high cloud resource cost overheads.

---

## Da real team: 

* **Aarushi** -
contact @ singhaarushi337@gmail.com
* **Praanjal** - 
contact @ praanjal17nov2007@gmail.com


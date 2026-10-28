---
area: 04_Curriculum
retrieved: 2026-10
source_fetched: '2026-10-28'
source_url: https://admission.cs.cityu.edu.hk/during-study/final-year-project-showcase/final-year-project-showcase-2025
status: draft
title: Final Year Project Showcase | CityUHK CS Admission
type: faq
vault: CityUHK-Undergraduate-FAQ
---

# Final Year Project Showcase | CityUHK CS Admission

> [!tip] Source
> Extracted from: https://admission.cs.cityu.edu.hk/during-study/final-year-project-showcase/final-year-project-showcase-2025
> Fetched: 2026-10-28

## Question

What does the official CityUHK page say about **Final Year Project Showcase | CityUHK CS Admission**?

## Answer

## Final Year Project Showcase

### Final Year Project Exhibition 2025

The Final Year Project (FYP) Exhibition was successfully held on 9 April 2025.

The event showcased the outstanding creativity, innovation, and research achievements of the graduating cohort. With a vibrant display of projects spanning multiple disciplines, attendees had the opportunity to engage with students and explore thought-provoking ideas at the forefront of their fields.

A highlight of the exhibition was the Best Poster Presentation Awards, celebrating excellence in both research content and visual communication. This year, five exceptional students were honored for their exemplary work: CABALLERO Rakichaz Calimbahin, HIRUNTEEYAKUL Maitree, HO Cheuk Hong, LI Hendry Wijaya, LUNG Lok Hin. Their posters captured the faculty’s attention for their clarity, originality, and impact, setting a high standard for future participants.

Best Poster Presentation Award Winners:

| Student Name: Supervisor: Project Title: | CABALLERO Rakichaz Calimbahin Prof. MA Chen Chess Puzzle Text2SQL | 
| Student Name: Supervisor: Project Title: | HIRUNTEEYAKUL Maitree Prof. LUO Yuhan A BLE and UWB Beacon-Assist Framework for Multiuser Augmented Reality Synchronization Across Multiple Devices in Shared Environments | 
| Student Name: Supervisor: Project Title: | HO Cheuk Hong Prof. IP Ho Shing Horace Lip Reading Model in Cantonese | 
| Student Name: Supervisor: Project Title: | LI Hendry Wijaya Prof. LEUNG Wing Ho Howard CityU Metaverse - Integrate and Expand Metaverse from User Content Contribution | 
| Student Name: Supervisor: Project Title: | LUNG Lok Hin Prof. LEUNG Wing Ho Howard 3D Object and Scene Creation for Metaverse | 


**FYP Poster of CABALLERO Rakichaz Calimbahin:**


**FYP Poster of HIRUNTEEYAKUL Maitree:**


[FYP Poster of] HO Cheuk Hong:


**FYP Poster of LI Hendry Wijaya**


**FYP Poster of LUNG Lok Hin:**


Congratulations to all the winners of the Best Poster Presentation Award, and heartfelt appreciation to their FYP supervisors: Prof. IP Ho Shing Horace, Prof. LEUNG Wing Ho Howard, Prof. LUO Yuhan, and Prof. MA Chen!

## Content Images (Vision)

### Image 5

This image is an academic project poster (CityU CS project 24CSG110) that describes a system called **Chess Puzzle Text2SQL**. It contains meaningful data, diagrams, and flowcharts.

Here is the structured breakdown of the poster's content:

### Project Metadata
*   **Institution:** CityU Department of Computer Science
*   **Project Code:** 24CSG110
*   **Name:** Siddhartha Rakshit
*   **Supervisor:** Prof. Adi Chen
*   **Product:** Chess Puzzle Text2SQL (website: www.chesspuzzletext2sql.com)

### 1. Introduction / Goal
*   The website allows users to search for chess puzzles using **Natural Language**.
*   **Example Queries:**
    *   "My friend began playing the French Defense, can you help me?"
    *   "Puzzles about sacrifice in the London"
    *   "Rating > 1900, Chess is Zugzwang"
*   **Access:** QR code provided on the poster.

### 2. How It Works (Text2SQL Pipeline)
The system uses a natural language processing technology to convert human text into SQL queries. The process is a 3-step linear flow:
1.  **Natural Question:** User inputs text (e.g., "Dutch Defense Midgame").
2.  **SQL Statement:** The system generates a query (e.g., `SELECT * FROM t_puzzle WHERE theme LIKE '%middlegame%' AND opening_tags LIKE '%Dutch Defense%'`).
3.  **Chess Puzzle:** The system returns the matching visual chessboard puzzle.

### 3. System Result & Utility
*   **Result:** The interface is Intuitive, Powerful, and User-friendly.
*   **Utility (Venn Diagram):** Text2SQL acts as a "glue" combining the **Ease of use of Search Engine** with the **Precision of Database Engine**.
*   **The "Takeaway":** A user does not need to know SQL or complex database queries; they can simply type natural language questions.

### 4. How It's Implemented
The poster details the technical methodology in a 3-step process:
*   **Step 1: Preface**
    *   State-of-the-art Text2SQL is done using LLM.
    *   *Problem:* Naive prompting of LLM is not very good, achieving only ~50% accuracy.
    *   *Solution:* "Have to be innovative."
*   **Step 2: Finding Similar Demonstrations**
    *   Using a prompt template is effective, but replacing static demonstrations with those **similar to the user's prompt** significantly boosts accuracy.
    *   *Constraint:* Finding similar demonstrations is "not easy to do" with semantic search.
*   **Step 3: Schema Masking**
    *   To support semantic search, the system replaces database keywords in queries with generalized forms (e.g., replacing a specific string with `<opening_tags>`).
    *   *Method:* Uses **Jaccard Similarity** to match these generalized queries.
    *   *Note:* 27 demonstrations were created synthetically for this project.

### 5. Benchmark / Results
*   **Final Accuracy:** **89.6%** (when using Finding Similar Demonstrations and Schema Masking).
*   *Comparison:* Accuracy drops to 82.9% if prompting without Schema Masking, and to 59.5% if prompting naively.
*   *Note:* Done on a self-made 1835 synthetic benchmark records.

## Source

- URL: https://admission.cs.cityu.edu.hk/during-study/final-year-project-showcase/final-year-project-showcase-2025
- Fetched: 2026-10-28
- Content hash: `8923874cd2036b84c8d08973b01349b0628008c4e77569945064152fd1f4e688`
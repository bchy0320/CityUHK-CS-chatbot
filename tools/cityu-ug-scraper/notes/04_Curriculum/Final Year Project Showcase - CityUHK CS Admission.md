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

This image is a poster for a CityU Computer Science undergraduate project titled **"Chess Puzzle Text2SQL"**. It is highly informational and contains a diagram, flowchart, and chart.

Here is a structured breakdown of its meaning:

### Project Details
*   **Institution:** Department of Computer Science, CityU (City University of Hong Kong).
*   **Course/Code:** CSD110 (listed under "Code").
*   **Supervisor:** Prof. Adi Chen.
*   **Website:** www.chesspuzzletext2sql.com

---

### 1. Core Concept: How Text2SQL Works (Flowchart)
The poster demonstrates a three-step process for converting natural language into a chess puzzle:
1.  **Natural Question:** User inputs text, e.g., *"Dutch Defense Midgame"*.
2.  **SQL Statement:** The system generates SQL code: `SELECT * FROM t_puzzle WHERE theme LIKE "%middlegame%" AND opening_tags LIKE "%Dutch Defense%"`.
3.  **Chess Puzzle:** The system retrieves and displays a corresponding chessboard image (puzzle).

---

### 2. Implementation Process (Steps 1, 2, 3)
A stylized "map" flowchart details the technical implementation:
*   **Step 1 (Preface):** Notes that using a basic LLM (Large Language Model) naively yields a low accuracy of ~50%. The goal is to be *innovative*.
*   **Step 2 (Finding Similar Demonstrations):** Uses a prompt template with static demonstrations. By replacing static demonstrations with ones *closely related to the user's prompt*, accuracy improves significantly. *Note: It admits that finding such similar demonstrations is a form of semantic search that is "not easy to do."*
*   **Step 3 (Schema Masking):** To support semantic search, database keywords are replaced with generalized forms (e.g., `"opening_tags"` becomes `<themes>`). The system then uses Jaccard Similarity to find matches.

---

### 3. Results and Advantages
*   **The Result:** A user interface that is **Intuitive, Powerful, and User-friendly**.
*   **The Takeaway:** The system acts as "glue," combining the **Ease of Use of a Search Engine** with the **Precision of a Database Engine**.

---

### 4. Data/Chart (Accuracy Benchmark)
The poster features a benchmark chart showing `89.6% Accuracy` for chess puzzles:
*   **With Schema Masking & Similar Demonstrations:** 89.6% (marked as *done on self-made 185 synthetic benchmark records*).
*   **Without Schema Masking (but with S.D.):** 82.9%.
*   **Naive Prompting:** 53.5%.

### Additional Information
*   **Example Queries:** Includes "My friend keeps playing the French Defense, can you help me?" and "Puzzle about sacrifice in the London".
*   **Access:** A QR code is provided to access the website via an IP address (details not fully readable).
*   **Note:** The poster explicitly states that "27 demonstrations created synthetically" were used.

## Source

- URL: https://admission.cs.cityu.edu.hk/during-study/final-year-project-showcase/final-year-project-showcase-2025
- Fetched: 2026-10-28
- Content hash: `8923874cd2036b84c8d08973b01349b0628008c4e77569945064152fd1f4e688`
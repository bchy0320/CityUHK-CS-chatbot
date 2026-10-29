# Notes 對比：原本就有的 notes vs 新增的 notes（網頁提取）

> **目的**：整理 Obsidian vault 中「原本就有的 notes」與 scraper 從 CityUHK 網頁提取的「新增 notes」之間的關係，指出重合內容與各自獨立於對面的內容。
>
> **範圍**：
> - **原本就有的 notes** = vault 根目錄（`00_Vault-Map` … `08_Scholarships`）的 **412 個** notes（已合併、已驗證）。
> - **新增的 notes（提取網頁）** = `tools/cityu-ug-scraper/notes/` 下的 **130 個** notes（`status: draft`，尚未合併進 vault）。
>
> **生成日期**：2026-10-29

---

## 一、原本就有的 notes（vault 根目錄，共 412 個）

### 00_Vault-Map（10 個）

| # | Note |
|---|------|
| 1 | CityUHK CS Academic Rankings and Reputation |
| 2 | CityUHK CS Admission at a Glance: Key Facts |
| 3 | CityUHK CS Admission FAQ Vault Map |
| 4 | CityUHK CS Programme Code Cheat Sheet |
| 5 | Is CityUHK CS a College of Computing Programme |
| 6 | JUPAS for CityUHK CS: The Big Picture |
| 7 | Vault Freshness and Verification Status |
| 8 | What Does the CS Department's Research Focus Mean for Students |
| 9 | Where to Find the Official Documents Cited in This Vault |
| 10 | Who Runs the CS Admissions Office and How to Contact |

### 01_JUPAS-Basics（16 個）

| # | Note |
|---|------|
| 1 | 1.5x Subject Weighting Policy (Draft) Status |
| 2 | CityUHK JUPAS Score Calculator |
| 3 | CityUHK Tuition Fees |
| 4 | How CityUHK Ranks Tied JUPAS Candidates |
| 5 | JS1204 2026 JUPAS Score Formula |
| 6 | JS1218 2026 JUPAS Score Formula |
| 7 | JUPAS 2027 Key Dates |
| 8 | JUPAS Application Steps |
| 9 | JUPAS Band Choices Explained |
| 10 | JUPAS Fees and Charges |
| 11 | JUPAS Flexible Admission Arrangement Explained |
| 12 | JUPAS Level Point Conversion Table |
| 13 | JUPAS Minimum Entrance Requirements for CS |
| 14 | JUPAS Score Conversion 5** 5* 5 4 3 2 1 |
| 15 | OEA and Principal's Nominations for CityUHK CS |
| 16 | Subject Weightings in JUPAS Admission Scores |

### 02_JUPAS-Scores（8 個）

| # | Note |
|---|------|
| 1 | JS1204 JUPAS Admission Score History |
| 2 | JS1218 BSc Cybersecurity Admission Score History |
| 3 | JS1221 Double Degree Admission Score History |
| 4 | JUPAS Admissions Scores: What Median and Lower Quartile Mean |
| 5 | JUPAS Score Calculator for CityUHK CS |
| 6 | Typical Admission Competitiveness: Most Admits Come From Band A |
| 7 | Why CityUHK CS Scores Are Not Comparable Across Years |
| 8 | Worked Example Computing JS1204 Admission Score |

### 03_NonJUPAS（10 個）

| # | Note |
|---|------|
| 1 | Advanced Standing I (Year 2) Admission |
| 2 | Advanced Standing II (Senior Year) Admission |
| 3 | BSc CS Non-JUPAS Code 1561A |
| 4 | BSc Cybersecurity Non-JUPAS Code 1720A |
| 5 | GCE A Level Admission to CS |
| 6 | General Entrance Requirements for Non-JUPAS |
| 7 | IB Diploma Admission to CS |
| 8 | Non-JUPAS Application Steps |
| 9 | Non-JUPAS Year 1 Admission |
| 10 | Transfer and Overseas Students to CityUHK CS |

### 04_Curriculum（18 個）

| # | Note |
|---|------|
| 1 | BSc Cybersecurity Curriculum |
| 2 | Calculus and Linear Algebra in CS |
| 3 | CS AI Stream Courses |
| 4 | CS Core Courses Explained |
| 5 | CS Data Science Stream Courses |
| 6 | CS Final Year Project Overview |
| 7 | CS First Year Courses and Credits |
| 8 | CS Multimedia and SE Stream Courses |
| 9 | CS Study Streams Explained |
| 10 | CS vs Cybersecurity: Key Differences |
| 11 | Curriculum of BSc Computer Science |
| 12 | Double Major and Minor Options in Computing |
| 13 | Internship Employers and Participating Companies |
| 14 | IT Professional Internship Overview |
| 15 | Minor in Artificial Intelligence |
| 16 | Minor in Computing |
| 17 | Software Engineering in the CS Curriculum |
| 18 | Why the Industry Internship Matters |

### 05_Programmes（14 個）

| # | Note |
|---|------|
| 1 | BSc Data Science vs CS Data Science Stream |
| 2 | CityUHK - Columbia Joint Bachelor's Degree |
| 3 | CS Career Prospects FAQ |
| 4 | Double Degree Requirements and Structure |
| 5 | JS1063 LLB and BSc Computer Science (AI) Double Degree Overview |
| 6 | JS1070 ACT Programme Overview |
| 7 | JS1071 Data Science Majors Overview |
| 8 | JS1072 BSc Data Science Overview |
| 9 | JS1074 BSc Data and Systems Engineering Overview |
| 10 | JS1204 BSc Computer Science Overview |
| 11 | JS1204 BSc Computer Science Streams List |
| 12 | JS1204 Graduate Employment Statistics |
| 13 | JS1218 BSc Cybersecurity Overview |
| 14 | JS1221 Double Degree Overview |

### 06_Courses（91 個）

每個 CS 課程一個 FAQ note（`CSxxxx ... Course FAQ`）：

```
CS1102, CS1103B, CS1302, CS1302A, CS1315, CS2066, CS2104, CS2115, CS2116,
CS2117, CS2204, CS2303, CS2310, CS2311, CS2312, CS2313, CS2315, CS2334,
CS2360, CS2402, CS2403, CS2468, CS2611, CS2612, CS2613, CS3000, CS3103,
CS3104, CS3185, CS3189, CS3201, CS3273, CS3283, CS3301, CS3334, CS3342,
CS3343, CS3346, CS3347, CS3356, CS3367, CS3382, CS3383, CS3391, CS3402,
CS3481, CS3483, CS3503, CS3504, CS3505, CS3612, CS4101, CS4182, CS4185,
CS4186, CS4187, CS4188, CS4191, CS4192, CS4273, CS4274, CS4280, CS4284,
CS4285, CS4286, CS4288, CS4289, CS4293, CS4295, CS4296, CS4297, CS4298,
CS4335, CS4348, CS4367, CS4381, CS4385, CS4386, CS4389, CS4394, CS4465,
CS4480, CS4482, CS4485, CS4486, CS4487, CS4489, CS4490, CS4493, CS4514,
CS4552
```

### 07_CityU-Scores（222 個）

每個 programme（JS code）× 年份（2023–2026）一個分數記錄 note。共 **63 個 programme**：

```
JS1000, JS1001, JS1002, JS1005, JS1007, JS1012, JS1013, JS1014, JS1017,
JS1018, JS1019, JS1025, JS1026, JS1027, JS1040, JS1041, JS1042, JS1043,
JS1044, JS1050, JS1051, JS1052, JS1053, JS1061, JS1062, JS1070, JS1071,
JS1072, JS1074, JS1100, JS1102, JS1103, JS1104, JS1106, JS1108, JS1109,
JS1110, JS1111, JS1112, JS1113, JS1122, JS1123, JS1200, JS1201, JS1202,
JS1204, JS1205, JS1206, JS1207, JS1208, JS1210, JS1211, JS1216, JS1217,
JS1218, JS1219, JS1220, JS1221, JS1300, JS1801, JS1805, JS1806, JS1807
```

> 每個 JS code 對應 2023、2024、2025、2026 四個年份的分數 note（部分年份缺漏）。

### 08_Scholarships（23 個）

| # | Note |
|---|------|
| 1 | AI Computing and Transformation (ACT) Flagship Scholarship |
| 2 | Can You Hold Multiple CityUHK Scholarships (No Concurrent Awards) |
| 3 | CityUHK Scholarship Overview |
| 4 | CityUHK Scholarships for Chinese Mainland Students |
| 5 | CityUHK Scholarships for Hong Kong Talents |
| 6 | College of Business Entrance Scholarship (BSc Computational Finance and FinTech) |
| 7 | Dean's Scholarships for JUPAS Entrants |
| 8 | Diversity Grant for International Students |
| 9 | Do Scholarships Change Which CS Programme to Choose |
| 10 | Entrance Scholarship Scheme for International Students |
| 11 | Flagship Scholarships for JUPAS Entrants |
| 12 | Flagship Scholarships for Non-JUPAS Entrants |
| 13 | HKSAR Government Scholarship Fund for Non-Local Students |
| 14 | How to Apply for CityUHK Entrance Scholarships (No Application Needed) |
| 15 | Institutional Scholarships for JUPAS Entrants |
| 16 | Institutional Scholarships for Non-JUPAS Entrants |
| 17 | Non-Local Tuition and Living Costs at CityUHK |
| 18 | Other Donor Scholarships and Prizes at CityUHK |
| 19 | Outstanding Athletes Entrance Scholarship for Non-Local Students |
| 20 | Scholarship HKDSE Scoring Scale |
| 21 | Scholarship Renewal and CGPA Requirements |
| 22 | Scholarship Timeline 2027 (JUPAS Entrants) |
| 23 | What Do Flagship Scholarship Recipients Get (Benefits) |

---

## 二、新增的 notes（scraper 網頁提取，共 130 個）

> 來源：`tools/cityu-ug-scraper/notes/`，全部為 `status: draft`，尚未合併進 vault。

### 01_JUPAS-Basics（14 個）

| # | Note | 來源 URL |
|---|------|---------|
| 1 | Admissions - City University of Hong Kong | cityu.edu.hk |
| 2 | Direct Application - Admission Interviews - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 3 | Direct Application - Admission Statistics - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 4 | Direct Application - Selection Steps - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 5 | Direct Application - Target Students - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 6 | JUPAS (HKDSE) - Admission Statistics - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 7 | JUPAS (HKDSE) - Entrance Requirements - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 8 | JUPAS (HKDSE) - JUPAS Interview - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 9 | JUPAS (HKDSE) - Major in Computer Science - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 10 | JUPAS (HKDSE) - Selection Criteria - CityUHK CS Admission | admission.cs.cityu.edu.hk |
| 11 | JUPAS Admission - CityUHK Admission | cityu.edu.hk |
| 12 | Non-JUPAS Senior Year Admission - CityUHK Admission | cityu.edu.hk |
| 13 | Non-JUPAS Year 1 Admission - CityUHK Admission | cityu.edu.hk |
| 14 | Undergraduate Admissions - City University of Hong Kong | cityu.edu.hk |

### 04_Curriculum（49 個）

| # | Note |
|---|------|
| 1 | Bachelor of Science in Computer Science - Curriculum - Degree Major Requirements |
| 2 | Bachelor of Science in Computer Science - Curriculum - Overview |
| 3 | Bachelor of Science in Computer Science - Curriculum - Study Plan |
| 4 | Bachelor of Science in Computer Science - Final Year Project Showcase 2026 |
| 5 | Bachelor of Science in Computer Science - IT Professional Internship - Employers |
| 6 | Bachelor of Science in Computer Science - IT Professional Internship - Overview |
| 7 | Bachelor of Science in Computer Science - IT Professional Internship - Participating Companies |
| 8 | Bachelor of Science in Computer Science - IT Professional Internship - Students |
| 9 | Bachelor of Science in Cybersecurity - Curriculum - Degree Major Requirements |
| 10 | Bachelor of Science in Cybersecurity - Curriculum - Overview |
| 11 | Bachelor of Science in Cybersecurity - Curriculum - Sample Study Schedule |
| 12 | Bachelor of Science in Cybersecurity - IT Professional Internship - Employers |
| 13 | Bachelor of Science in Cybersecurity - IT Professional Internship - Overview |
| 14 | Bachelor of Science in Cybersecurity - IT Professional Internship - Students |
| 15 | Career Opportunity - CityUHK CS Admission |
| 16 | Career Paths - CityUHK CS Admission |
| 17 | Curriculum & Study Plan - CityUHK CS Admission |
| 18 | Employment Sector - CityUHK CS Admission |
| 19 | Final Year Project Showcase - CityUHK CS Admission |
| 20 | Final Year Project Showcase - CityUHK CS Admission (2) |
| 21 | Inbound Student Exchange Course List - Exchange Course List |
| 22 | International Exposure and Co-Curricular Learning - CityUHK CS Admission |
| 23 | IT Professional Internship (ITPI) - CityUHK CS Admission |
| 24 | Master of Philosophy / Doctor of Philosophy in Computer Science - Curriculum - Overview |
| 25 | Master of Philosophy / Doctor of Philosophy in Computer Science - Curriculum - Structures |
| 26 | Master of Science in Artificial Intelligence - Curriculum |
| 27 | Master of Science in Computer Science - Curriculum - Overview |
| 28 | Master of Science in Computer Science - Curriculum - Schedule |
| 29 | Master of Science in Computer Science - Curriculum - Structures |
| 30 | Master of Science in Cybersecurity - Curriculum |
| 31 | Master of Science in Electronic Commerce - Curriculum - Overview |
| 32 | Master of Science in Electronic Commerce - Curriculum - Schedule |
| 33 | Master of Science in Electronic Commerce - Curriculum - Structures |
| 34 | Minor in Artificial Intelligence - Aims |
| 35 | Minor in Artificial Intelligence - Application |
| 36 | Minor in Artificial Intelligence - Curriculum - Structures |
| 37 | Minor in Computing - Aims |
| 38 | Minor in Computing - Application |
| 39 | Minor in Computing - Curriculum - Overview |
| 40 | Minor in Computing - Curriculum - Overview (2) |
| 41 | Minor in Computing - Curriculum - Structures |
| 42 | Minor in Computing - Faq |
| 43 | Postgraduate Certificate in Information Security - Curriculum - Overview |
| 44 | Postgraduate Certificate in Information Security - Curriculum - Structures |
| 45 | Student Exchange - Department of Computer Science |
| 46 | Student Mentoring - Department of Computer Science |
| 47 | Student Mentoring - Department of Computer Science (2) |
| 48 | Study Streams - CityUHK CS Admission |
| 49 | TEN Common Myths - CityUHK CS Admission |

### 05_Programmes（39 個）

| # | Note |
|---|------|
| 1 | Alumni Sharing - Department of Computer Science |
| 2 | Bachelor of Science in Computer Science - Admissions - Admissions Direct Non Jupas |
| 3 | Bachelor of Science in Computer Science - Admissions - Admissions Hkdse Students |
| 4 | Bachelor of Science in Computer Science - Aims |
| 5 | Bachelor of Science in Computer Science - Contact Us |
| 6 | Bachelor of Science in Computer Science - Graduate Employment Statistics |
| 7 | Bachelor of Science in Cybersecurity - Admissions - Admissions Direct Non Jupas |
| 8 | Bachelor of Science in Cybersecurity - Admissions - Admissions Hkdse Students |
| 9 | Bachelor of Science in Cybersecurity - Aims |
| 10 | Bachelor of Science in Cybersecurity - Contact Us |
| 11 | Double Degree Programme - BSC Computer Science And BSC Computational Finance |
| 12 | Double Degree Programme - Degree Major Requirements |
| 13 | Double Degree Programme - Suggested Study Plan |
| 14 | Joint Bachelor's Degree Program - Department of Computer Science |
| 15 | Master of Philosophy / Doctor of Philosophy in Computer Science - Admissions |
| 16 | Master of Philosophy / Doctor of Philosophy in Computer Science - Aims |
| 17 | Master of Philosophy / Doctor of Philosophy in Computer Science - Contact Us |
| 18 | Master of Science in Artificial Intelligence - Admissions |
| 19 | Master of Science in Artificial Intelligence - Aims |
| 20 | Master of Science in Artificial Intelligence - Faq |
| 21 | Master of Science in Artificial Intelligence - Financial Aids |
| 22 | Master of Science in Computer Science - Admissions |
| 23 | Master of Science in Computer Science - Aims |
| 24 | Master of Science in Computer Science - Faq |
| 25 | Master of Science in Computer Science - Financial Aids |
| 26 | Master of Science in Cybersecurity - Admissions |
| 27 | Master of Science in Cybersecurity - Aims |
| 28 | Master of Science in Cybersecurity - Faq |
| 29 | Master of Science in Cybersecurity - Financial Aids |
| 30 | Master of Science in Electronic Commerce - Admissions |
| 31 | Master of Science in Electronic Commerce - Aims |
| 32 | Master of Science in Electronic Commerce - Contact Us |
| 33 | Master of Science in Electronic Commerce - Departments |
| 34 | Master of Science in Electronic Commerce - Faq |
| 35 | Master of Science in Electronic Commerce - Financial Aids |
| 36 | Postgraduate Certificate in Information Security - Admissions |
| 37 | Postgraduate Certificate in Information Security - Aims |
| 38 | Postgraduate Certificate in Information Security - Education Loan |
| 39 | Programmes Overview - Department of Computer Science |

### 06_Courses（1 個）

| # | Note |
|---|------|
| 1 | Programme and Course Catalogue - City University of Hong Kong |

### 08_Scholarships（4 個）

| # | Note |
|---|------|
| 1 | Bachelor of Science in Computer Science - IT Professional Internship - IT Internship Awards |
| 2 | Bachelor of Science in Computer Science - Scholarships |
| 3 | Minor in Computing - Award |
| 4 | Scholarships - City University of Hong Kong |

### 09_Undergraduate-General（1 個）

| # | Note |
|---|------|
| 1 | Department of Computer Science |

### 11_People-Faculty（22 個）

| # | Note |
|---|------|
| 1 | Academic Staff - Department of Computer Science |
| 2 | Antoni Bert CHAN |
| 3 | Cong WANG |
| 4 | Dapeng WU |
| 5 | Gerhard Petrus HANCKE |
| 6 | Hau San WONG |
| 7 | Jianping WANG |
| 8 | Jun WANG |
| 9 | Junhui HOU |
| 10 | Lusheng WANG |
| 11 | Minming LI |
| 12 | Nan GUAN |
| 13 | Qingfu ZHANG |
| 14 | Shengdong ZHAO |
| 15 | Shiqi WANG |
| 16 | Shuaicheng LI |
| 17 | Wei-Ying MA |
| 18 | Weifa LIANG |
| 19 | Xiaohua JIA |
| 20 | Xiaotie DENG |
| 21 | Yuguang FANG |
| 22 | Zhenjiang LI |

---

## 三、重合內容（兩邊都有相同主題）

> 以下主題在「原本就有的 notes」與「新增的 notes」中**都出現**。新增 notes 是從官方網頁提取的原始內容（`status: draft`），原本 notes 是已整理、已驗證的 FAQ（`status: verified`）。兩者主題對應，但**詳略與結構不同**。

| 主題 | 原本就有的 notes（vault） | 新增的 notes（scraper） |
|------|--------------------------|------------------------|
| **JUPAS 入學要求** | JUPAS Minimum Entrance Requirements for CS | JUPAS (HKDSE) - Entrance Requirements |
| **JUPAS 面試** | JUPAS for CityUHK CS: The Big Picture（Q7 提及） | JUPAS (HKDSE) - JUPAS Interview |
| **JUPAS 選拔標準** | Subject Weightings in JUPAS Admission Scores | JUPAS (HKDSE) - Selection Criteria |
| **JUPAS 統計** | JS1204 / JS1218 / JS1221 Admission Score History | JUPAS (HKDSE) - Admission Statistics；Direct Application - Admission Statistics |
| **非JUPAS Year 1** | Non-JUPAS Year 1 Admission | Non-JUPAS Year 1 Admission |
| **非JUPAS Senior Year** | Advanced Standing I / II Admission | Non-JUPAS Senior Year Admission |
| **BSc CS 課程** | Curriculum of BSc Computer Science | BSc Computer Science - Curriculum（Overview / Degree Major Requirements / Study Plan） |
| **BSc Cybersecurity 課程** | BSc Cybersecurity Curriculum | BSc Cybersecurity - Curriculum（Overview / Degree Major Requirements / Sample Study Schedule） |
| **IT Professional Internship** | IT Professional Internship Overview；Internship Employers and Participating Companies | BSc CS / BSc Cyber - IT Professional Internship（Overview / Employers / Participating Companies / Students）；IT Professional Internship (ITPI) |
| **Study Streams** | CS Study Streams Explained | Study Streams - CityUHK CS Admission |
| **Minor in AI** | Minor in Artificial Intelligence | Minor in Artificial Intelligence（Aims / Application / Curriculum Structures） |
| **Minor in Computing** | Minor in Computing | Minor in Computing（Aims / Application / Curriculum / Faq） |
| **Double Degree** | Double Degree Requirements and Structure；JS1221 Double Degree Overview | Double Degree Programme（Degree Major Requirements / Suggested Study Plan / BSC CS & BSC Computational Finance） |
| **Joint Bachelor's Degree** | CityUHK - Columbia Joint Bachelor's Degree | Joint Bachelor's Degree Program |
| **Career / 就業前景** | CS Career Prospects FAQ | Career Opportunity；Career Paths |
| **Employment Sector** | JS1204 Graduate Employment Statistics | Employment Sector；BSc CS - Graduate Employment Statistics |
| **Final Year Project** | CS Final Year Project Overview | Final Year Project Showcase（多個） |
| **Scholarships** | 08_Scholarships（23 個） | Scholarships - City University of Hong Kong；BSc CS - Scholarships；Minor in Computing - Award；IT Internship Awards |
| **BSc CS 概覽** | JS1204 BSc Computer Science Overview | BSc Computer Science - Aims |
| **BSc Cybersecurity 概覽** | JS1218 BSc Cybersecurity Overview | BSc Cybersecurity - Aims |
| **Admissions 概覽** | JUPAS for CityUHK CS: The Big Picture 等 | Admissions - City University of Hong Kong；Undergraduate Admissions；JUPAS Admission |
| **Contact / 聯絡** | Who Runs the CS Admissions Office and How to Contact | BSc CS / BSc Cyber - Contact Us |

---

## 四、各自獨立於對面的內容

### 4.1 新增的 notes 獨有（vault 中沒有對應主題）

這些是 scraper 從網頁提取、**vault 完全沒有**的新主題：

| 主題 | 新增 notes 數量 | 說明 |
|------|----------------|------|
| **研究生課程（MSc / MPhil / PhD / PgCert）** | ~40 個 | MSc AI、MSc CS、MSc Cybersecurity、MSc Electronic Commerce、MPhil/PhD、Postgraduate Certificate in Information Security（含 Admissions / Aims / Curriculum / Faq / Financial Aids / Education Loan 等） |
| **教授 / 教職員頁面** | 22 個 | 11_People-Faculty：Academic Staff + 21 位教授個人頁面 |
| **Student Exchange（學生交換）** | 2 個 | Student Exchange；Inbound Student Exchange Course List |
| **Student Mentoring（導師制）** | 2 個 | Student Mentoring（×2） |
| **Alumni Sharing（校友分享）** | 1 個 | Alumni Sharing |
| **Programme and Course Catalogue** | 1 個 | 課程目錄 |
| **Department of Computer Science 概覽** | 1 個 | 09_Undergraduate-General |
| **TEN Common Myths（十大迷思）** | 1 個 | TEN Common Myths |
| **International Exposure and Co-Curricular Learning** | 1 個 | 國際交流與課外學習 |

### 4.2 原本就有的 notes 獨有（scraper 中沒有對應主題）

這些是 vault 中**已有、但 scraper 未提取**的內容：

| 主題 | 原本 notes 數量 | 說明 |
|------|----------------|------|
| **91 個 CS 課程 FAQ** | 91 個 | 06_Courses：每個 CS 課程一個詳細 FAQ（scraper 只有 1 個課程目錄 note） |
| **222 個分數記錄** | 222 個 | 07_CityU-Scores：63 個 programme × 2023–2026 分數（scraper 只有 admission statistics 概覽） |
| **JUPAS 分數計算器 / 公式** | 多個 | CityUHK JUPAS Score Calculator、JS1204/JS1218 2026 Score Formula、JUPAS Score Conversion、Level Point Conversion Table、Worked Example |
| **1.5× Subject Weighting Policy** | 1 個 | 1.5x Subject Weighting Policy (Draft) Status |
| **JUPAS Band Choices / OEA / 日期 / 費用** | 多個 | JUPAS Band Choices Explained、OEA and Principal's Nominations、JUPAS 2027 Key Dates、JUPAS Fees and Charges、CityUHK Tuition Fees |
| **非JUPAS 細節** | 多個 | BSc CS Non-JUPAS Code 1561A、BSc Cybersecurity Non-JUPAS Code 1720A、GCE A Level Admission、IB Diploma Admission、Transfer and Overseas Students |
| **課程細節** | 多個 | CS Core Courses Explained、CS First Year Courses and Credits、Calculus and Linear Algebra in CS、Software Engineering in the CS Curriculum、CS vs Cybersecurity: Key Differences、Double Major and Minor Options |
| **Programme 細節** | 多個 | JS1063 LLB & BScCS、JS1070 ACT、JS1071/JS1072/JS1074 Data Science、BSc Data Science vs CS Data Science Stream、JS1204 Streams List |
| **獎學金細節** | 23 個 | 08_Scholarships 的詳細獎學金 note（scraper 只有 4 個概覽） |
| **Vault 地圖 / 索引** | 10 個 | 00_Vault-Map：Vault Map、Programme Code Cheat Sheet、Key Facts、Freshness Status 等 |

---

## 五、總結

| 類別 | 數量 |
|------|------|
| 原本就有的 notes（vault） | 412 |
| 新增的 notes（scraper 提取） | 130 |
| **重合**（scraper notes 與 vault 主題對應） | 63 個 scraper notes |
| **新增獨有**（scraper 有、vault 無） | 67 個 scraper notes（研究生課程 36、教授 22、交換 2、導師 2、校友 1、目錄 1、系所 1、迷思 1、國際交流 1） |
| **原本獨有**（vault 有、scraper 無） | ~340 個 vault notes（91 課程 FAQ、222 分數記錄、JUPAS 計算器/公式、獎學金細節等） |

### 重點觀察

1. **重合部分**：新增 notes 是官方網頁的**原始提取**（`status: draft`），原本 notes 是**已整理驗證**的 FAQ（`status: verified`）。兩者主題對應，但新增 notes 更貼近官方原文，原本 notes 更精煉、含交叉連結與「Short answer」提示。

2. **新增獨有**：scraper 大幅擴展了 vault 的範圍，新增了**研究生課程**（MSc/MPhil/PhD/PgCert）、**教授/教職員**、**學生交換/導師制**、**校友分享**、**十大迷思**等原本沒有的主題——這正是「從 CS Admission FAQ 擴展到更廣泛的本科/研究生資訊」的目標。

3. **原本獨有**：vault 擁有 scraper 未覆蓋的**大量細節**——91 個課程 FAQ、222 個分數記錄、JUPAS 計算器/公式/轉換表、詳細獎學金 note 等。這些是 vault 的核心價值，scraper 的概覽型 notes 無法取代。

4. **建議**：合併時應以「原本 notes 為骨架、新增 notes 補充官方原文細節」為原則，避免重複；新增的 draft notes 需人工審查後再提升為 `verified`。
# Modern PFE CV (AI & Data Engineering) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform Anas Mouquine's CV into a state-of-the-art, modern 1-page LaTeX CV tailored for 5th-year AI & Data Engineering PFE (Projet de Fin d'Études) internship recruiting, integrating extracted top-tier projects, verified credentials, and the COSUMAR internship.

**Architecture:** A modern asymmetric two-column LaTeX layout (`geometry`, `tcolorbox`, `titlesec`, `enumitem`, `hyperref`, `fontawesome5`) with sleek typography, curated color tokens, tag pills for technical stacks, and clickable links for portfolio, GitHub, LinkedIn, and Coursera certificates. Fits perfectly on 1 page with zero overflow.

**Tech Stack:** LaTeX (pdflatex/xelatex), TikZ/tcolorbox, FontAwesome 5, Modern Typeface (Helvetica/Modern Sans), Hyperref.

---

### Task 1: Extraction & Content Synthesis (AI & Data PFE Focus)

**Files:**
- Create: `docs/content_synthesis.md`
- Inspect: `portfolio_script.js`, `My Resume (2).pdf`

**Step 1: Curate the most impactful AI & Data projects from portfolio & PDF**
- Project 1: **AI Multi-Agent Orchestrator** (LangChain, Python, RAG, FastAPI, Subagents, Vector Search, Automated QA Benchmarking).
- Project 2: **Enterprise Media Lakehouse & Real-Time ETL Platform** (Apache Airflow, Medallion Architecture Bronze/Silver/Gold, Docker, Kafka, Data Validation).
- Project 3: **Film-A / Graph-Based AI Engine** (React Native, Neo4j Graph DB, Gemini AI / LLM Reasoning, Node.js REST API).

**Step 2: Structure professional experiences (including COSUMAR)**
- Experience 1: **COSUMAR – Stage Ingénieur / Data & Systèmes Industriels** (Casablanca): Industrial data collection, automated ETL reporting, KPI consolidation, and process monitoring.
- Experience 2: **SEWS-CABINET (Sumitomo Electric) – Stage Développeur Mobile & IoT** (07/2025 – 09/2025): SEWS Connect, real-time WebRTC audio/video, QR workstation scanner, first-scan-wins task claiming, Hive offline cache.

**Step 3: Curate top-tier certifications from the 11 verified Coursera credentials**
- Select the 5 most respected and relevant certificates for AI/Data PFE recruiters:
  1. *Agile Project Management* (Google, 2024)
  2. *Software Engineering: Design & Management* (HKUST, 2024)
  3. *Using Python to Access Web Data & APIs* (Univ. of Michigan, 2024)
  4. *Programmation Orientée Objet en C++* (EPFL, 2024)
  5. *Advanced React & State Architecture* (Meta, 2024)

**Step 4: Commit synthesis document**
- Verify alignment with PFE recruiter expectations.

---

### Task 2: Architecture & Layout Design of the Modern LaTeX CV

**Files:**
- Create: `cv_modern_pfe.tex`

**Step 1: Set up modular geometry, color palette, and micro-typography**
- Margin: 0.9cm – 1.0cm for optimal 1-page density.
- Palette: Modern Executive Slate (`#0F172A`), Tech Indigo (`#4338CA`), Accent Cyan (`#0284C7`), Neutral Muted (`#475569`), Light Card Tint (`#F8FAFC`).
- Two-column balanced structure:
  - **Left / Main Column (63% width):** Professional Summary (Targeting AI & Data PFE), Professional Experience (Cosumar, SEWS), High-Impact AI/Data Projects.
  - **Right / Sidebar Column (35% width):** Contact details with live clickable links, Education (EMSI 5ème année Informatique & Réseaux - IA & Data Science, Bac), Technical Skills grouped by domain (AI/ML, Big Data & Lakehouse, Core Backend & Cloud, Mobile/Frontend), Top Verified Certifications with direct verification links, Languages.

**Step 2: Define custom formatting macros**
- `\cvtag{}` for pill-style technology badges.
- `\cvevent{title}{organization}{date}{location}` for consistent experience/education headers.
- `\cvproject{title}{tech stack}{github link}` for clean project showcase.

---

### Task 3: Content Population & Fine-Tuning for 1-Page Constraint

**Files:**
- Modify: `cv_modern_pfe.tex`

**Step 1: Insert refined French/English text tailored for Moroccan & International PFE recruiting**
- Header: Anas Mouquine, Élève Ingénieur en 5ème Année – Spécialisation Intelligence Artificielle & Data Science.
- Clear mention of seeking a 4 to 6 months Stage PFE (disponible pour le PFE 2026).
- Add active hyperlinks with FontAwesome 5 icons for LinkedIn, GitHub, and Portfolio (`https://anasmouquinee.github.io/port/`).

**Step 2: Detail COSUMAR & SEWS internship tasks with action verbs & measurable impact**
- COSUMAR: Pipelines de données, automatisation de reporting, monitoring industriel.
- SEWS: Flutter, WebRTC, QR scanning, temps réel, collaboration d'équipe.

**Step 3: Document AI & Big Data projects with exact architectural keywords**
- LangChain, RAG, Subagents, Airflow, Medallion Architecture, Neo4j, Docker.

---

### Task 4: Compilation, Validation & Visual Inspection

**Files:**
- Compile: `cv_modern_pfe.tex` -> `cv_modern_pfe.pdf`
- Generate preview images: Python script using `pdf2image` or `fitz` (PyMuPDF) or TeX utilities to generate high-resolution PNG of the compiled PDF.

**Step 1: Compile with pdflatex**
- Command: `pdflatex -interaction=nonstopmode cv_modern_pfe.tex`
- Ensure 0 errors and 0 critical warnings.

**Step 2: Verify page count**
- Ensure strictly 1 page (no spillover to page 2).

**Step 3: Visual inspection**
- Inspect margins, alignment, typography contrast, and visual balance.

---

### Task 5: Delivery & User Instructions

**Files:**
- Create: `README.md` explaining how to compile, customize, and adapt the LaTeX source code.
- Present summary of extracted projects, certifications, and improvements over the previous version.

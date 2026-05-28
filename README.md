# Threatscope

**An Explainable AI-Driven SIEM for Early-Stage Cyber Threat Intelligence**

> MSc Thesis Project | Swami Vivekananda University | 2025 – Present

---

## The problem

SOC analysts deal with thousands of alerts a day. Most SIEM tools flag threats but offer no explanation — just an alert with a severity label. Analysts either investigate everything and burn out, or start ignoring alerts and miss real incidents.

The core issue is not detection. It is explainability.

## What Threatscope does

Threatscope is a SIEM that applies machine learning with explainable AI (XAI) to catch threats at early stages — before escalation — and tells the analyst exactly why each alert fired.

- Detects threats early using ML classification on ingested log data
- Assigns a confidence score to every alert
- Outputs the reasoning behind each detection (feature importance, decision rationale)
- Reduces false positive noise and analyst alert fatigue

Analysts get actionable context, not just a red flag.

---

## Architecture

```
Network / System Logs
        |
   Log Ingestion
        |
  Feature Extraction
        |
   ML Classifier  ──────────────────────────────┐
        |                                        |
    XAI Layer (SHAP / LIME)              Confidence Score
        |                                        |
   Alert Dashboard  ◄───────────────────────────┘
   (Explanation + Score + Recommended Action)
```

---

## Tech stack

| Component | Technology |
|-----------|------------|
| Log processing | Python, ELK Stack |
| ML model | Scikit-learn |
| Explainability | SHAP / LIME |
| Data pipeline | Python (custom ingestion scripts) |
| OS | Kali Linux / Ubuntu |

---

## Key features

- Early-stage detection before threats escalate
- Explainable outputs — every alert has a reason
- Confidence scoring per detection
- Designed to reduce SOC analyst cognitive load
- Not a black box

---

## Results

> To be updated on thesis completion — detection accuracy, false positive reduction rate, and comparison against baseline SIEM tools.

---

## Run locally

```bash
git clone https://github.com/Twilightpixie/Threatscope
cd Threatscope
pip install -r requirements.txt
python main.py
```

---

## Status

Active development — MSc thesis project (2025 – Present)

---

**Sristi Ghosh** | Sristixwork@gmail.com | [LinkedIn](https://www.linkedin.com/in/sristighosh-work2003/)

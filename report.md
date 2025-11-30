```markdown
# Kasparro Agentic Facebook Performance Analyst  
## Technical Report

---

## 1. Introduction

This project implements a fully autonomous **multi-agent system** designed to perform Facebook Ads performance analysis.  
The goal is to automatically diagnose **why ROAS changed over time**, identify contributing performance drivers, and recommend **new creative directions** for low-CTR campaigns.

The system uses structured agent prompts, JSON-based communication, and numerical evaluation to ensure measurable, explainable insights.

---

## 2. Problem Statement

Digital advertisers often struggle to interpret complex Facebook Ads metrics.  
ROAS fluctuations can arise from various factors such as:

- Audience fatigue  
- Creative underperformance  
- CTR declines  
- Geographic or platform shifts  
- Poor conversion rate  
- Spending inefficiencies  

Manually diagnosing these issues is slow and subjective.  
This system solves that by enabling an **AI-driven, multi-agent analyst**.

---

## 3. System Architecture

The system contains **five specialized agents**, orchestrated to collaborate end-to-end.

### **3.1 Planner Agent**
- Interprets user question  
- Breaks it into structured subtasks  
- Assigns tasks to the appropriate agents  
- Ensures JSON-schema compliance  

### **3.2 Data Agent**
- Receives only dataset summaries (not raw rows)  
- Produces human-readable insights  
- Highlights trends in ROAS, CTR, spend, and creatives  

### **3.3 Insight Agent**
- Generates hypotheses explaining performance changes  
- Uses chain-of-thought reasoning internally  
- Outputs clean, structured hypotheses  

### **3.4 Evaluator Agent**
- Tests hypotheses using numeric statistics  
- Determines support level: *yes / no / partial*  
- Highlights key performance drivers  
- Identifies which segments caused the ROAS shift  

### **3.5 Creative Improvement Generator**
- Analyzes high-CTR patterns (tone, value prop, CTA)  
- Recommends new creatives for low-CTR campaigns  
- Suggests headlines, body text, CTAs  
- Provides rationale grounded in dataset evidence  

---

## 4. Data Summary Strategy

To adhere to assignment rules:

- **The entire CSV is never passed to the LLM**  
- Only **aggregated summaries** are shared:
  - ROAS by date  
  - CTR trends  
  - Spend/revenue totals  
  - Top campaigns  
  - Low-CTR creative messages  
  - High-CTR creative examples  

These summaries are prepared in code via pandas before being given to the agents.

---

## 5. Hypothesis Evaluation Logic

The Evaluator Agent uses:
- ROAS deltas over time  
- CTR change percentages  
- Spend shifts  
- ROAS by campaign and audience  
- Best/worst-performing creatives  

Example evaluation metrics:
- ROAS % change (start → end)
- CTR drop correlation with ROAS drop
- High spend / low return campaigns
- Audience-type performance differences

The agent compares hypotheses with these metrics and categorizes them as:

- **Supported**  
- **Partially supported**  
- **Not supported**  

---

## 6. Creative Strategy

Low-CTR campaigns are examined for:
- Weak value proposition
- Lack of urgency
- Generic messaging
- Poor alignment with high-performing patterns

High-CTR creatives are analyzed for:
- Tone (urgency, emotional appeal, FOMO)
- Value props (discounts, limited-time offers)
- Effective CTAs
- Audience segmentation

The Creative Agent generates:
- 2–3 new headlines  
- 1–2 improved body texts  
- 1–2 optimized CTAs  
- Rationale based on high-CTR insights  

---

## 7. Results Summary

The system outputs:

### **insights.json**
- Planner’s task breakdown  
- Data summaries  
- Hypotheses  
- Evaluation results  
- A unified narrative explaining ROAS change  

### **creatives.json**
- New creative ideas for each low-CTR campaign  
- Reasons for each suggestion  
- Patterns learned from top-performing creatives  

### **logs.txt**
- Step-by-step pipeline logs  
- Useful for debugging  

---

## 8. Strengths, Limitations & Future Work

### **Strengths**
- Fully autonomous multi-agent reasoning  
- JSON-structured outputs  
- Real numeric evaluation from dataset  
- Creative recommendations grounded in data  
- Minimal LLM token usage through summarization  

### **Limitations**
- Evaluation depends on numeric summary quality  
- Creative suggestions limited by dataset diversity  
- Time windows are fixed (30-day default)  

### **Future Enhancements**
- Auto-selecting impactful time windows  
- Anomaly detection for sudden ROAS drops  
- Multi-platform analysis (Meta + Google Ads)  
- Real Facebook Ads API integration  
- Visualization dashboards  

---

## 9. Conclusion

This project successfully demonstrates an **Agentic AI Facebook Performance Analyst**, capable of:

- Diagnosing ROAS changes  
- Evaluating performance drivers  
- Proposing creative improvements  
- Producing structured, explainable outputs  

It fulfills all requirements of the Kasparro assignment and showcases how multi-agent systems can automate complex marketing analytics tasks at scale.

---

# Kasparro Agentic Facebook Performance Analyst  
A Multi-Agent System for Automated ROAS Diagnosis & Creative Recommendation

This repository contains a fully working **Agentic AI system** designed for the Kasparro Applied AI Engineer Assignment.  
It autonomously analyzes Facebook Ads performance, diagnoses why ROAS changes over time, and recommends improved creative messaging for low-CTR campaigns.

---

## 🚀 Project Overview

This system uses **five AI agents**, each with a specialized role:

### **1. Planner Agent**
Breaks the user question into structured subtasks for other agents.

### **2. Data Agent**
Summarizes the dataset (no raw CSV passed to LLM), focusing on:
- ROAS changes  
- CTR trends  
- Spend/revenue patterns  
- Low-CTR campaigns  
- Creative performance  

### **3. Insight Agent**
Produces hypotheses explaining ROAS fluctuations using structured reasoning.

### **4. Evaluator Agent**
Tests each hypothesis using computed statistics and determines if they are:
- Supported  
- Partially supported  
- Not supported  

### **5. Creative Improvement Generator**
Creates new ad messages, headlines, and CTAs for low-performing campaigns,
grounded in high-CTR patterns from the dataset.

---

## 🧩 Core Features

- Autonomous multi-agent orchestration  
- Structured JSON outputs:
  - `insights.json`  
  - `creatives.json`
- Data summarization without exposing full CSV to LLM  
- Real, analyzable ROAS trends  
- Creative idea generation based on performance patterns  
- Clean, reproducible dataset summaries  
- Log tracking (`outputs/logs.txt`)

---

## 📁 Repository Structure
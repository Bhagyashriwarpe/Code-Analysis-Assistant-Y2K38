# 🛡️ CodeGuard AI – Code Analysis Assistant

An AI-powered code analysis assistant that uses Machine Learning to classify code according to its potential **Year 2038 (Y2038) vulnerability risk**.

The system analyzes code written in **C, C++, and Java** and categorizes the potential risk into:

- 🟢 **Low Risk**
- 🟠 **Medium Risk**
- 🔴 **High Risk**

---

## 🚀 Features

- 🤖 Machine Learning-based code risk classification
- 🔍 Detects potential Y2038-related code risks
- 🧠 Uses TF-IDF for text feature extraction
- ⚡ Uses Linear SVM for classification
- 💻 Supports C, C++, and Java code
- 🌐 Simple and attractive web interface
- 🔗 Frontend and ML backend integration using Flask REST API
- 📊 Classifies code into Low, Medium, and High risk levels

---

## 🏗️ Project Architecture

```text
┌──────────────────────────────┐
│          Frontend             │
│       HTML + CSS + JS         │
└──────────────┬───────────────┘
               │
               │ HTTP POST Request
               ▼
┌──────────────────────────────┐
│        Flask Backend          │
│           app.py              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       TF-IDF Vectorizer       │
│   Converts code into features │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Linear SVM Model        │
│      Risk Classification       │
└──────────────┬───────────────┘
               │
               ▼
      Low / Medium / High Risk
